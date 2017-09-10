#!/usr/bin/python

import random
#from secret import FLAG 
import base64
import binascii

KEY = 'musZTXmxV58UdwiKt8Tp'

def xor_str(x, y):
    if len(x) > len(y):
        return ''.join([chr(ord(z) ^ ord(p)) for (z, p) in zip(x[:len(y)], y)])
    else:
        return ''.join([chr(ord(z) ^ ord(p)) for (z, p) in zip(x, y[:len(x)])])

#FLAG = open('flag.enc', 'rb').read()
flag = open('flag.enc', 'r').read()
#flag, key = FLAG.encode('hex'), KEY.encode('hex')
key = KEY.encode('hex')
enc = xor_str(key * (len(flag) // len(key) + 1), flag).encode('hex')

x = enc.decode('hex')
print x
for i in xrange(0, len(x), 2):
    print chr(int(x[i] + x[i+2], 16)),
#print base64.b64decode(enc.decode('hex'))
#print enc
#print binascii.b2a_hex(x)

#ef = open('flag.enc', 'w')
#ef.write(enc.decode('hex'))
#ef.close()