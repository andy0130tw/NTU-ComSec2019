#!/usr/bin/env python3
# from sympy import *
import random

def op1(p, s):
    return sum([i * j for i, j in zip(s, p)]) % 256

def op2(m, k):
    return bytes([i ^ j for i, j in zip(m, k)])

def op3(m, p):
    return bytes([m[p[i]] for i in range(len(m))])

def op4(m, s):
    return bytes([s[x] for x in m])

'''
Linear Feedback Shift Register
'''
def stage0(m):
    random.seed('oalieno')
    p = [int(random.random() * 256) for i in range(16)]
    s = [int(random.random() * 256) for i in range(16)]
    c = b''
    for x in m:
        k = op1(p, s)
        c += bytes([x ^ k])
        s = s[1:] + [k]
    return c

'''
Substitution Permutation Network
'''
def stage1(m):
    random.seed('oalieno')
    k = [int(random.random() * 256) for i in range(16)]
    p = [i for i in range(16)]
    random.shuffle(p)
    s = [i for i in range(256)]
    random.shuffle(s)

    c = m
    for i in range(16):
        c = op2(c, k)
        c = op3(c, p)
        c = op4(c, s)
    return c

def encrypt(m, key):
    stage = [stage0, stage1]
    for i in map(int, '{:08b}'.format(key)):
        m = stage[i](m)
    return m


def main():
    enc = open('encrypted', 'rb').read()
    ans = b'F'
    for i in range(1, 16):
        print('i=', i)
        for g in range(128):
            test = (ans + bytes([g]) + b'\x00' * 16)[:16]
            # print('test', test)
            cand = set()
            for k in [31, 79, 103, 115, 121, 124]:
                x = encrypt(test, k)
                if enc[:(i+1)] == x[:(i+1)]:
                    cand.add(k)
            if cand:
                print('cand for g=', g, cand)
                ans += bytes([g])
                print('ans', ans)
                break


if __name__ == '__main__':
    main()
    # flag = open('flag', 'rb').read()
    # assert(len(flag) == 16)
    # key = open('key', 'rb').read()
    # assert(E ** ( I * pi ) + len(key) == 0)
    # open('cipher', 'wb').write(encrypt(flag, int.from_bytes(key, 'little')))
