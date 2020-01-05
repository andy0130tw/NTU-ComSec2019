#!/usr/bin/python3.6

# modified from
# https://github.com/sasdf/ctf/blob/master/tasks/2018/ais3Final/crypto/200-secureSub/_files/solution/ga.py

import random
import json
import functools as fn
import numpy as np
import readline
import string
import hashlib

charset = string.ascii_lowercase + string.digits + ',. '
charset_idmap = {e: i for i, e in enumerate(charset)}

ksz = 80

def decrypt(ctx, key):
    N, ksz = len(charset), len(key)
    return ''.join(charset[(c - key[i % ksz]) % N] for i, c in enumerate(ctx))


print("""
It may converge to local optima, Run it several times until
the plaintext is clear enough to recover manually.
""")


def toPrintable(data):
    ul = ord('_')
    data = bytes(c if 32 <= c < 127 else ul for c in data)
    return data.decode('ascii')


# -- Loading data -- #
with open('./output.txt', 'r') as f:
    ctx = f.readline().strip()[4:]
    enc = bytes.fromhex(f.readline().strip()[6:])
ctx = [charset_idmap[c] for c in ctx]

with open('ngrams.json') as f:
    ngrams = json.load(f)

@fn.lru_cache(10000)
def get_trigram(x):
    x = ''.join(x)
    y = ngrams.get(x)
    if y is not None:
        return y

    ys = []
    a, b = ngrams.get(x[:2]), ngrams.get(x[2:])
    if a is not None and b is not None:
        ys.append(a + b)
    a, b = ngrams.get(x[:1]), ngrams.get(x[1:])
    if a is not None and b is not None:
        ys.append(a + b)
    if len(ys):
        return max(ys)
    if any(c not in ngrams for c in x):
        return -25
    return sum(map(ngrams.get, x))


@fn.lru_cache(10000)
def fitness(a):
    plain = decrypt(ctx, a)
    tgs = zip(plain, plain[1:], plain[2:])
    score = sum(get_trigram(tg) for tg in tgs)
    return score


def initialize(size):
    population = []
    for i in range(size):
        key = tuple(random.randrange(len(charset)) for _ in range(ksz))
        population.append(key)
    return population


def crossover(a, b, prob):
    r = list(a)
    for i in range(len(r)):
        if random.random() < prob:
            r[i] = b[i]
    return tuple(r)


def mutate(a):
    r = list(a)
    i = random.randrange(len(a))
    r[i] = random.randrange(len(charset))
    return tuple(r)


def select(population, size):
    scores = np.array([fitness(p) for p in population])
    scores = np.exp(scores - scores.max()) + 1e-300
    scores = scores / scores.sum()
    idx = np.random.choice(len(population), size, replace=False, p=scores)
    return [population[i] for i in idx]


def truncate(population, size):
    population = population[:]
    population.sort(key=lambda x: -fitness(x))
    population = population[:size]
    return population


#-- Run Genetic Algorithm --#
population = initialize(1000)
for iter in range(1000):
    try:
        best = population[0]
        plain = decrypt(ctx, best)
        score = fitness(best)
        print(f'[Iter {iter:5d}] {score:10.2f}:  {plain}')
        for p in select(population[1:], 20):
            c = crossover(best, p, 0.5)
            population.append(c)
            for i in range(5):
                m = mutate(c)
                population.append(m)
        population = list(set(population))
        population = truncate(population, 1000)
    except KeyboardInterrupt:
        break
key = list(population[0])


# -- Manually fix -- #
print('')
print('Manually fix')
print('h, l: move cursor, j / k: dec/inc key, q: quit')
off = 0
while True:
    score = fitness(tuple(key))
    plain = decrypt(ctx, key)
    print('Score:', score)
    print(' ' * off + 'v')
    for i in range(0, len(plain), ksz):
        print(plain[i:i+ksz])
    print(' ' * off + '^')

    cmd = input('> ').encode('ascii')
    if cmd == b'h':
        off = max(off - 1, 0)
    elif cmd == b'l':
        off = min(off + 1, ksz - 1)
    elif cmd == b'j':
        key[off] = (key[off] - 1) % len(charset)
    elif cmd == b'k':
        key[off] = (key[off] + 1) % len(charset)
    elif cmd == b'q':
        break
    else:
        print('Incorrect input')

k = hashlib.sha512(''.join(charset[k] for k in key).encode('ascii')).digest()
dec = bytes(ci ^ ki for ci, ki in zip(enc, k))

print('dec =', dec)

#
# Score: -2444.63806041798
#                                                              v
# according to cnn, when researchers were asked what their language of choice was,
#  40 percent of the unicorns chose english. the other 60 percent of the unicorns
# chose a language that could not be given a simple answer. the research says that
#  more than a third of unicorns only use english. some are even creating whole la
# nguage systems.
#                                                              ^
