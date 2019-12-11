#!/usr/bin/env python3
import hashlib
import sys
from multiprocessing import (Pool, Event, Process)


def is_valid(N, prefix, expecting, idx, halt):
    i = idx
    expLen = len(expecting)

    while not halt.is_set():
        s = prefix + str(i)
        digest = hashlib.md5(s.encode()).digest()

        bits = ''.join(hex(i)[2:].zfill(2) for i in digest)
        if bits[:expLen] == expecting:
            print(i)
            halt.set()

        i += N

def main():
    if len(sys.argv) < 3:
        print('Usage: {} <prefix> <expecting>'.format(sys.argv[0]))
        return

    halt = Event()

    prefix = sys.argv[1]
    expecting = sys.argv[2]

    N = 8

    for z in range(N):
        p = Process(target=is_valid, args=(N, prefix, expecting, z, halt))
        p.start()

    halt.wait()

if __name__ == '__main__':
    main()
