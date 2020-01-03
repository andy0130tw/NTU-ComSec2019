import binascii
import subprocess
from math import gcd

from pwn import *

context.proxy = (socks.SOCKS5, 'localhost', 8888)

def unhex(m):
    return binascii.unhexlify(hex(m)[2:]).decode()

def xgcd(a,b):
    prevx, x = 1, 0;  prevy, y = 0, 1
    while b:
        q, r = divmod(a,b)
        x, prevx = prevx - q*x, x
        y, prevy = prevy - q*y, y
        a, b = b, r
    return a, prevx, prevy

def get_int_with_prefix(prefix):
    p.recvuntil(prefix)
    return int(p.recvline().strip())

# def factor(n):
#     print('Factoring N=%d' % n)
#     cmd = 'display2d:false;factor(%d);' % n
#     out = subprocess.getoutput(['maxima', '-r', cmd])
#     return out[out.index('(%o2)') + 5 : out.index('(%i3)')].strip()

def pollardPm1(n):
    a = 2
    b = 2
    while True:
        a = pow(a, b, n)
        d = gcd(a - 1, n)
        if 1 < d < n:
            print('b=', b)
            return d
        b += 1



p = remote('edu-ctf.csie.org', 10191)

p.sendlineafter('>', '1')

c = get_int_with_prefix('c = ')
e = get_int_with_prefix('e = ')
n = get_int_with_prefix('n = ')

print('c = %d' % c)
print('e = %d' % e)
print('Factoring N = %d' % n)
p = pollardPm1(n)
q = n // p
assert p * q == n

m = (p-1) * (q-1)
_, _, d = xgcd(m, e)
d += m

print(unhex(pow(c, d, n)))
