"""
from subprocess import Popen, PIPE

def read_until_prompt(p):
    inp = ""
    while not inp.endswith("(gdb) "):
        inp += p.stdout.read(1)
    #print inp
    return inp

def try_a_flag(flag, p):
    p.stdin.write("run " + flag + "\n")
    read_until_prompt(p)
    #p.stdin.write("y\n")
    p.stdin.write("x/s $rdi\n")
    rdi = read_until_prompt(p)
    return rdi

def get_esi(flag, p):
    p.stdin.write("run " + flag + "\n")
    read_until_prompt(p)
    p.stdin.write("x/s $esi\n")
    esi = read_until_prompt(p)
    return esi

def get_gdb_val(s):
    return s.split(' ')[1]

def make_string(n):
    s = str(n)
    s = s.zfill(6)
    return "0"*3+s

p = Popen(["gdb", "abc"], bufsize=0, stdout=PIPE, stdin=PIPE)
read_until_prompt(p)

p.stdin.write("break *0x400B77\n")
read_until_prompt(p)

esi = get_esi(make_string(0), p)
for i in range(999999):
#for i in range(5):
    inp = try_a_flag(make_string(i), p)
    #print inp
    if i % 100 == 0:
        print float(i)/float(999999)
    if inp == esi:
        print "flag: ", make_string(i)
        exit(0)


#print p.stdout.readline()

# the first 3 numbers don't matter?
#print try_a_flag("0" * 29)
#print try_a_flag("0" * 3 + "1" + "0" * 25)
#print try_a_flag("1" * 3 + "1" + "0" * 25)
#print try_a_flag("1" * 3 + "1" + "0" * 5)
#print try_a_flag("1" * 3 + "1" + "1" * 5)
#print try_a_flag("1" * 3 + "1" + "1" * 6)
#for i in range(9):
"""

iv = [0x67452301, 0x0EFCDAB89, 0x98BADCFE, 0x10325476, 0x0C3D2E1F0, 0]