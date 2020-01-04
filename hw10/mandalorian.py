import binascii
import subprocess
from math import gcd

from pwn import *

# context.proxy = (socks.SOCKS5, 'localhost', 8888)

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


p = remote('edu-ctf.csie.org', 10192)

p.sendlineafter('>', '1')

c = get_int_with_prefix('c = ')
e = get_int_with_prefix('e = ')
n = get_int_with_prefix('n = ')

t = 0

_, _, inv_of_16 = xgcd(n, 16)
assert inv_of_16 * 16 % n == 1

sub = 0

inv_of_16k = 1

print('Round ', end='')
for nround in range(1024 // 4):
    print('%d ' % nround, end='')
    p.sendlineafter('>', '2')
    payload = pow(inv_of_16k, e, n) * c
    p.sendline(str(payload % n))
    m = get_int_with_prefix('m = ')

    # sub_k = inv16^k x_0 + inv16^(k-1) x_1 + ... + inv16^0 x_k
    # => sub_{k+1} = inv16 (sub_k + x_k)
    x = (m - (sub % n)) % 16
    t += x << (nround * 4)

    sub = inv_of_16 * (sub + x)
    inv_of_16k = inv_of_16k * inv_of_16 % n

print('END!')
print(unhex(t))
