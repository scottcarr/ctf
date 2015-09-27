from random import randint, choice
import numpy as np
start_deck = [ 0, 7, 7, 7, 8, 8, 8, 8, 8, 8, 32]
start_hand = [ 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0 ]
dealer_start_hand = [ 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0 ]

N_ITERATIONS = 100000

def total_hand(hand):
    total = sum([x * y for (x, y) in enumerate(hand)])
    if hand[1] > 0 and total <= 11:
        total += 10
    return total

def make_deck(deck):
    cards = []
    for i, val in enumerate(deck):
        if val == 0:
            pass
        else:
            cards.extend([i]*val)
    return cards


def dealer_monte_carlo(deck):
    results = []
    for i in xrange(N_ITERATIONS): 
        cards = make_deck(deck)
        hand = list(dealer_start_hand)
        while True:
            card = choice(cards)
            cards.remove(card)
            hand[card] += 1
            total = total_hand(hand)
            if total >= 17:
                results.append(total)
                break
    y = np.bincount(np.asarray(results))
    ii = np.nonzero(y)[0]
    #tbl = np.asarray(np.vstack((ii, y[ii])).T, dtype=float)
    tbl = zip(ii, y[ii])

    new_tbl = []
    new_cnt = 0
    for val, cnt in tbl:
        if val < 22:
            new_tbl.append((val,cnt))
        else:
            new_cnt += cnt

    new_tbl.append(('bust', new_cnt))

    freq_tbl = []
    for val, cnt in new_tbl:
        freq_tbl.append((val, float(cnt)/float(N_ITERATIONS)))

    print freq_tbl

    #print new_tbl

    #tot_bust = 0
    #for val in tbl[:,0]:
    #    if val > 21:
    #        tot += tbl[val,1]

    #freq = tbl[:5,1] / N_ITERATIONS
    #print freq

    #tbl2 = np.hstack((tbl, freq.T))
    #print tbl2
    return freq_tbl

def getCard(card, deck, hand):
    hand[card] += 1
    deck[card] -= 1

def isBust(hand):
    return 21 < sum([x * y for (x, y) in enumerate(hand)])

def countValidHands(deck, hand):
    if isBust(hand):
        return 0

    validHands = 0
    #dealer_probs = dealer_monte_carlo(list(deck))

    my_score = total_hand(hand)

    win_prob = dealer_sim(deck, list(dealer_start_hand), my_score)
    #win_prob = 0
    #for val, prob in dealer_probs:
    #    if val == 'bust' or my_score > val:
    #        win_prob += prob
    #for i, prob in enumerate(dealer_probs):
    #    if i == 0 or my_score > i:
    #        win_prob += prob

    for i in xrange(len(start_deck)):
        if (deck[i] > 0):
            hand_clone = [x for x in hand]
            deck_clone = [x for x in deck]
            getCard(i, deck_clone, hand_clone)
            validHands += float(deck[i])/float(sum(deck))*countValidHands(deck_clone, hand_clone)

    return max(win_prob, validHands)


def dealer_sim(deck, hand, my_score):
    if isBust(hand):
        return 1.0

    validHands = 0
    #dealer_probs = dealer_monte_carlo(list(deck))

    dealer_score = total_hand(hand)

    if dealer_score >= 17:
        if dealer_score < my_score:
            return 1.0
        else:
            return 0.0

    for i in xrange(len(start_deck)):
        if (deck[i] > 0):
            hand_clone = [x for x in hand]
            deck_clone = [x for x in deck]
            getCard(i, deck_clone, hand_clone)
            validHands += float(deck[i])/float(sum(deck))*dealer_sim(deck_clone, hand_clone, my_score)

    return validHands

#dealer_probs = np.load("dealer_probs3.npy")

#tbl = [.3748]
#tbl.extend([0.0]*16)
#tbl.append(.1307)
#tbl.append(.1202)
#tbl.append(.1210)
#tbl.append(.1164)
#tbl.append(.1131)
##print tbl
#dealer_probs = np.asarray(tbl)
##print dealer_probs
        

print countValidHands(start_deck, start_hand)
#print dealer_monte_carlo(start_deck)

