from random import randint
import numpy as np
from itertools import product

DEBUG = False
N_DEALER_SIMS = 50000000
#N_PLAYER_SIMS = 1000000
#N_DEALER_SIMS = 100
N_PLAYER_SIMS = 1000000
#N_PLAYER_SIMS = 1

FACE_CARDS = ['A', 'K', 'Q', 'J']
NUMBER_CARDS = map(str, range(2, 11))
ONE_SUITS_CARDS = FACE_CARDS + NUMBER_CARDS
POSSIBLE_DEALER_RESULTS = [17, 18, 19, 20, 21, -1]

BUSTED = -1
HIT = -2

#dealer_probs = {}

fname = "dealer_probs3.npy"

class Deck:
    def __init__(self):
        self.cards = ONE_SUITS_CARDS * 4 * 2
    def remove(self, card):
        self.cards.remove(card)
    def deal(self):
        deal_idx = randint(0,len(self.cards)-1)
        dealt_card = self.cards[deal_idx]
        self.cards.remove(dealt_card)
        return dealt_card

#deck = Deck()

#print len(deck.cards)

dealer_face_up_card = '3'
my_starting_cards = ['A', '2']

def is_face(card):
    return FACE_CARDS.count(card) > 0

def simulate_dealer():
    dealer_sim_results = [0]*N_DEALER_SIMS
    for i in range(N_DEALER_SIMS):
        dealer_sim_results[i] = simulate_dealer_once()
    return dealer_sim_results
    
def get_dealer_decision(dealer_hand):

    totals, hands = total_hand(dealer_hand)

    useable_hands = filter(is_not_busted, totals)

    if len(useable_hands) == 0:
        return BUSTED

    best = max(useable_hands)

    if best >= 17:
        return best

    return HIT

def simulate_dealer_once():
    decision = HIT
    deck = Deck()
    deck.remove(dealer_face_up_card)
    deck.remove('A')
    deck.remove('2')
    decision, hand = simulate_dealer_hand(deck)
    return decision

def simulate_dealer_hand(deck):
    dealer_hand = [dealer_face_up_card]

    while True: 
        dealer_hand.append(deck.deal())
        decision = get_dealer_decision(dealer_hand)
        if decision != HIT:
            break
    return decision, dealer_hand

def total_hand(hand):
    #print "hand : ", hand
    # the hand can have any number of aces!!
    n_aces = hand.count('A')
    possible_values = [x for x in product([1,11], repeat = n_aces)]
    hands = []
    totals = []
    for prod in possible_values:
        tmp_hand = list(prod)
        tmp_hand.extend([c for c in hand if c != 'A'])
        #hands.append(.extend([c for c in hand if c != 'A']))
        #print tmp_hand
        hands.append(tmp_hand)
    for val in possible_values:
        t = sum(val)
        for card in hand:
            if card == 'A':
                pass # we already totalled the aces
            elif is_face(card):
                t += 10
            else:
                t += int(card)
        totals.append(t)
    #print "hand totals: ", totals
    return totals, hands

def is_busted(total):
    return total >= 22

def is_not_busted(total):
    return total <= 21

class DecisionTable:
    def __init__(self, dealer_file):
        self.dealer_probs = np.load(dealer_file)
        #print self.dealer_probs
    def getWinProb(self, score):
        prob = np.copy(self.dealer_probs[0])
        if score > 20:
            prob += self.dealer_probs[20]
        if score > 19:
            prob += self.dealer_probs[19]
        if score > 18:
            prob += self.dealer_probs[18]
        if score > 17:
            prob += self.dealer_probs[17]
        return prob
    def getLoseProb(self, score):
        ## you can never win when the dealer gets 21
        prob = np.copy(self.dealer_probs[21])
        if score <= 20:
            prob += self.dealer_probs[20]
        if score <= 19:
            prob += self.dealer_probs[19]
        if score <= 18:
            prob += self.dealer_probs[18]
        if score <= 17:
            prob += self.dealer_probs[17]
        #prob = self.dealer_probs[0]
        #if score > 17:
        #    prob += self.dealer_probs[17-1]
        #if score > 18:
        #    prob += self.dealer_probs[18-1]
        #if score > 19:
        #    prob += self.dealer_probs[19-1]
        #if score > 20:
        #    prob += self.dealer_probs[20-1]
        ## you can never win when the dealer gets 21
        return prob

def save_numpy_file(sim_res):
    """
    my_possible_scores = range(3, 22)
    dealer_possible_scores = range(17, 22)
    print dealer_possible_scores
    print my_possible_scores
    arr = np.zeros((22,22), dtype=float)
    prob_map = {}
    for score in POSSIBLE_DEALER_RESULTS:
        tmp = sim_res.count(score)
        tot = len(sim_res)
        prob_map[score] = float(tmp) / float(tot)

    for mine in my_possible_scores:
        for dealer in dealer_possible_scores:
            prob = prob_map[-1]
            if mine > 17:
                prob += prob_map[17]
            if mine > 18:
                prob += prob_map[18]
            if mine > 19:
                prob += prob_map[19]
            if mine > 20:
                prob += prob_map[20]
            arr[dealer, mine] = prob
    arr[21,:] = np.ones((1,22)) #if I don't bust and he does I win
    arr[21,21] = 0.0 # if we both bust I lose
    print arr[20,:]
    """
    dealer_probs = np.zeros((22,1), dtype=float)
    for score in POSSIBLE_DEALER_RESULTS:
        tmp = sim_res.count(score)
        tot = len(sim_res)
        if score != -1:
            dealer_probs[score] = float(tmp) / float(tot)
        else:
            dealer_probs[0] = float(tmp) / float(tot)
    np.save(fname, dealer_probs)

def simulate_player():
    wins = 0
    for i in range(N_PLAYER_SIMS):
        deck = Deck()
        deck.remove(dealer_face_up_card)
        for card in my_starting_cards:
            deck.remove(card)
        player_score, player_hand = simulate_player_hand(deck)
        dealer_score, dealer_hand = simulate_dealer_hand(deck)
        if DEBUG:
            print "dealer hand: ",dealer_hand
            print dealer_score
            print "my hand: ", player_hand
            print player_score
        if player_score > dealer_score:
            wins += 1
    return float(wins) / float(N_PLAYER_SIMS)


def filter_busted_hands(totals, hands):
    new_totals = []
    new_hands = []
    for i in range(len(totals)):
        if totals[i] <= 21:
            new_totals.append(totals[i])
            new_hands.append(hands[i])
    return new_totals, new_hands

#def pick_best_hand(totals, hands):
#    totals, hands = filter_busted_hands(totals, hands)
#    soft_totals, soft_hands, no_soft_totals, no_soft_hands = filter_soft_ace_hands(totals, hands)
#
#    best_soft_total = max(soft_totals)
#    best_no_soft_total = max(no_soft_totals)
#
#    best = max(best_soft_total, best_no_soft_total)
#
#    if best >= 17:
#        
#
#    if best_soft_total >= 17:
#        idx = np.argmax(no_soft_totals)
#        tot = no_soft_totals[idx]


def filter_soft_ace_hands(totals, hands):
    soft_ace_totals = []
    soft_ace_hands = []
    no_soft_ace_totals = []
    no_soft_ace_hands = []
    for i in range(totals, hands):
        if hands[i].count(11) > 0:
            soft_ace_hands.append(hands[i])
            soft_ace_totals.append(totals[i])
        else:
            no_soft_ace_hands.append(hands[i])
            no_soft_ace_totals.append(totals[i])
    return soft_ace_totals, soft_ace_hands, no_soft_ace_totals, no_soft_ace_hands
    


def simulate_player_hand(deck):
    tbl = DecisionTable("dealer_probs.npy")
    #print tbl.dealer_probs
    hand = list(my_starting_cards) # may a copy
    totals, hands = total_hand(hand)
    totals, hands = filter_busted_hands(totals, hands)

    # check if I busted
    if len(totals) == 0:
        return BUSTED, hand 

    stand_win_probs = map(tbl.getWinProb, totals)
    max_idx = np.argmax(stand_win_probs)
    stand_win_prob = stand_win_probs[max_idx][0]
    stand_win_total = totals[max_idx]
    stand_win_hand = hands[max_idx]


    #print "stand_win_prob: ", stand_win_prob
    #print "stand_win_total: ", stand_win_total
    #print totals
    #print stand_win_hand

    #totals = total_hand(hand)
    #best_total = max(totals)
    #shouldStay = stand_win_prob > .5 or (not has_soft_ace(stand_win_hand) and stand_win_total >= 17)
    #shouldStay = stand_win_total >= 17 and not has_soft_ace(stand_win_hand)

    #shouldHit = stand_win_total <= 12 or (stand_win_total <= 18 and has_soft_ace(stand_win_hand))

    #print hand
    #print stand_win_total
    while (stand_win_total <= 11 and stand_win_prob < .5) \
            or (stand_win_total < 17 and has_soft_ace(stand_win_hand)):
        if DEBUG:
            print "stand_win_prob: ", stand_win_prob
            print "stand_win_total: ", stand_win_total
            print has_soft_ace(stand_win_hand)
            #print totals
            #print stand_win_hand
            print "HIT"
        hand.append(deck.deal())
        if DEBUG:
            print hand
        totals, hands = total_hand(hand)

        # check if I busted
        totals, hands = filter_busted_hands(totals, hands)
        if len(totals) == 0:
            print "BUSTED"
            return BUSTED, hand 

        #for total in totals:
        #    lose_prob = tbl.getLoseProb(total)
        #    if lose_prob < best_prob:
        #        best_total = total
        #        best_prob = lose_prob
        stand_win_probs = map(tbl.getWinProb, totals)
        max_idx = np.argmax(stand_win_probs)
        stand_win_prob = stand_win_probs[max_idx]
        stand_win_total = totals[max_idx]
        stand_win_hand = list(hands[max_idx])
        #shouldStay = stand_win_total >= 17
        shouldHit = stand_win_total <= 12 or stand_win_total <= 18 and has_soft_ace(stand_win_hand)

    #print hand
    #print totals
    #print lose_probs
    #print best_total

    if DEBUG:
        print "stopping at:"
        print stand_win_prob
        print stand_win_total
    return stand_win_total, stand_win_hand

def has_soft_ace(hand):
    return hand.count(11) > 0

def main():

    #sim_dealer = True
    sim_dealer = False

    if sim_dealer:
        sim_res = simulate_dealer()
        save_numpy_file(sim_res)

    tbl = DecisionTable("dealer_probs3.npy")
    hit_win_prob = simulate_player()
    #stand_win_prob = tbl.getWinProb(13)[0]
    stand_win_prob = .3748 # from the internet
    print "prob of winning if hit: {:.4f}".format(hit_win_prob)
    print "prob of winning if stay: {:.4f}".format(stand_win_prob)
    print "TMCTF{{HIT:{:.4f}:STAND:{:.4f}}}".format(hit_win_prob, stand_win_prob)
    #tbl = DecisionTable("dealer_probs.npy")
    #print tbl.dealer_probs
    #print sum(tbl.dealer_probs)

    #for mine in range(3,22):
    #    print "prob of me losing if I have {0}: {1}".format(mine, tbl.getLoseProb(mine))

main()
#tbl = DecisionTable("dealer_probs.npy")
#totals, hands = total_hand(['A', 2, '6'])
#print filter_busted_hands(totals, hands)
#stand_win_probs = map(tbl.getWinProb, totals)
#print stand_win_probs
#max_idx = np.argmax(stand_win_probs)
#stand_win_prob = stand_win_probs[max_idx]
#stand_win_total = totals[max_idx]
#stand_win_hand = list(hands[max_idx])
#print stand_win_hand

"""
sim_res = simulate_dealer()
tbl = DecisionTable(sim_res)
stand = "{:.4f}".format(tbl.getWinProb(13))
hit = "{:.4f}".format(tbl.getLoseProb(13))
"""





