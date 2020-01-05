import random
import os
import math
import functools
import itertools
from pprint import pprint
import heapq
import copy
from spn_side import SPN, int2bits
import numpy as np
import ast
import hashlib


random.seed(42)
nround = 4
key = os.urandom(8)

with open('./output.txt') as f:
    sbox = ast.literal_eval(f.readline().split('=')[1].strip())
    pbox = ast.literal_eval(f.readline().split('=')[1].strip())

    lines = f.read().splitlines()
    enc = bytes.fromhex(lines.pop()[6:])

cipher = SPN(sbits=4, nblock=16, nround=nround)
cipher.set_boxes(sbox, pbox)

sbits, nbits = cipher.sbits, cipher.nbits
N = 1 << sbits

data = []
for x, y in zip(lines[::2], lines[1::2]):
    x = bytes.fromhex(x[4:])
    y = int(y[4:])
    data.append((x, y))



# Start attack

sbox = {int(k, 2): int(v, 2) for k, v in cipher.sbox.items()}
sbox = [sbox[i] for i in range(len(sbox))]
sbox = np.array(sbox, dtype=int)
# x -> sbox[x]

sums = [sum(map(int, bin(i)[2:])) for i in range(N)]
sums = np.array(sums, dtype=int)
# x -> #1(x)

ssbox = np.sign(sums[sbox] - (sbits / 2)).astype(int)
# x -> #1(sbox[x]) > (max(#1) / 2) \in {-1, 0, 1}

X, Y = [], []
for x, y in data:
    x = int2bits(int.from_bytes(x, 'little'), nbits)
    x = [int(x[i:i+sbits], 2) for i in range(0, nbits, sbits)]
    X.append(x)
    Y.append(y)
X = np.array(X, dtype=int).T
Y = np.array(Y, dtype=int)
# X: block -> i -> input
# Y: i -> count


# truth = int2bits(int.from_bytes(key, 'little'), nbits)
# truth = [int(truth[i:i+sbits], 2) for i in range(0, nbits, sbits)]
rkeys = []
for i in range(cipher.nblock):
    results = []
    # [(score, block key), ...]

    for k in range(N):
        m = ssbox[np.arange(N, dtype=int) ^ k]
        bias = m[X[i]]
        pos, neg = Y[bias == 1].mean(), Y[bias == -1].mean()
        results.append((pos - neg, k))

    results = sorted(results)[::-1]
    print('    '.join(f'{k:x}: {s:.2f}' for s, k in results[:5]))
    # assert truth[i] == results[0][1]
    rkeys.append(results[0][1])


# print flag
rkeyi = ''.join(hex(c)[2:] for c in rkeys)
rkeyi = bytes.fromhex(rkeyi)[::-1]
k = hashlib.sha512(rkeyi).digest()
dec = bytes(ci ^ ki for ci, ki in zip(enc, k))
print('dec =', dec)
