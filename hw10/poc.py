#!/usr/bin/env python3
from Crypto.Util.number import *


p = 10007293440455865537573894696048871066962912884836681524976625984704129340017677234997403655890126488881500871210614121606584901286821378456930012907566217
q = 10532856311338001188322378920389633976948841099223345903050449506977302169261538895314076311388748242257921099120281184329227485537541079708356104877502357

flag = b'Decrypt succeed!!!'
# '0x446563727970742073756363656564212121'

def xgcd(a,b):
    prevx, x = 1, 0;  prevy, y = 0, 1
    while b:
        q, r = divmod(a,b)
        x, prevx = prevx - q*x, x
        y, prevy = prevy - q*y, y
        a, b = b, r
    return a, prevx, prevy


def genkeys():
    e = 65537
    while True:
        # p, q = getPrime(512), getPrime(512)
        n, phi = p * q, (p - 1) * (q - 1)
        if GCD(e, phi) == 1:
            d = inverse(e, phi)
            return (n, e), (n, d)

def menu():
    print(f'{" menu ":=^20}')
    print('1) info')
    print('2) decrypt')

def info(pub):
    n, e = pub
    m = bytes_to_long(flag)
    c = pow(m, e, n)
    return c, e, n

def decrypt_oracle(inp, pri):
    n, d = pri
    c = inp
    m = pow(c, d, n)
    return m % (2 ** 4)

def main():
    pub, pri = genkeys()
    c, e, n = info(pub)

    t = 0

    _, _, inv_of_16 = xgcd(n, 16)
    assert inv_of_16 * 16 % n == 1

    sub = 0

    inv_of_16k = 1
    for nround in range(1024 // 4):
        payload = pow(inv_of_16k, e, n) * c
        m = decrypt_oracle(payload % n, pri)

        # sub_k = inv16^k x_0 + inv16^(k-1) x_1 + ... + inv16^0 x_k
        # => sub_{k+1} = inv16 (sub_k + x_k)
        x = (m - (sub % n)) % 16
        t += x << (nround * 4)

        sub = inv_of_16 * (sub + x)
        inv_of_16k = inv_of_16k * inv_of_16 % n

    print('result', long_to_bytes(t))

main()
