import random
import hashlib
import os
import functools
from pprint import pprint


def int2bits(x, nbits):
    x = bin(x)[2:].rjust(nbits, '0')
    assert len(x) == nbits
    return x


class SPN(object):
    def __init__(self, sbits, nblock, nround):
        self.sbits = sbits
        self.nblock = nblock
        self.nround = nround
        self.nbits = self.sbits * self.nblock

    def random_gen(self):
        sbox = list(range(1 << self.sbits))
        pbox = list(range(self.nbits))
        random.shuffle(sbox)
        random.shuffle(pbox)
        sbox = {
            int2bits(i, self.sbits): int2bits(e, self.sbits)
            for i, e in enumerate(sbox)}
        self.set_boxes(sbox, pbox)

    def set_boxes(self, sbox, pbox):
        self.sbox = sbox
        self.pbox = pbox
        self.isbox = {e: i for i, e in self.sbox.items()}
        self.ipbox = {e: i for i, e in enumerate(self.pbox)}
        self.ipbox = [self.ipbox[i] for i in range(len(self.ipbox))]

    def set_key(self, key):
        keys = [key]
        for _ in range(self.nround):
            key = hashlib.sha256(key).digest()
            key = int.from_bytes(key, 'little')
            key = int(int2bits(key, 256)[:self.nbits], 2)
            key = key.to_bytes((self.nbits + 7) // 8, 'little')
            keys.append(key)
        self.set_raw_keys(keys)

    def set_raw_keys(self, keys):
        assert len(keys) == self.nround + 1
        self.raw_keys = keys
        self.keys = [int.from_bytes(k, "little") for k in keys]
        self.keys = [int2bits(k, self.nbits) for k in self.keys]
        ipkeys = [self.permute(k, self.ipbox) for k in self.keys[::-1]]
        self.invkeys = self.keys[-1:] + ipkeys[1:-1] + self.keys[:1]

    def add_round_key(self, x, k):
        return int2bits(int(x, 2) ^ int(k, 2), self.nbits)

    def substitute(self, x, sbox):
        return ''.join(
            sbox[x[block: block+self.sbits]]
            for block in range(0, self.nbits, self.sbits))

    def permute(self, x, pbox):
        return ''.join(x[i] for i in pbox)

    def run(self, x, sbox, pbox, keys):
        x = int2bits(int.from_bytes(x, "little"), self.nbits)
        for round, k in enumerate(keys[:-1]):
            x = self.add_round_key(x, k)
            x = self.substitute(x, sbox)
            if round != self.nround - 1:
                x = self.permute(x, pbox)
        x = self.add_round_key(x, keys[-1])
        x = int(x, 2).to_bytes((self.nbits + 7) // 8, "little")
        return x

    def encrypt(self, x):
        return self.run(x, self.sbox, self.pbox, self.keys)

    def decrypt(self, x):
        return self.run(x, self.isbox, self.ipbox, self.invkeys)


sbox_paths = [[8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, -2, -2, 0, 0, -2, 6, 2, 2, 0, 0, 2, 2, 0, 0],
     [0, 0, -2, -2, 0, 0, -2, -2, 0, 0, 2, 2, 0, 0, -6, 2],
     [0, 0, 0, 0, 0, 0, 0, 0, 2, -6, -2, -2, 2, 2, -2, -2],
     [0, 2, 0, -2, -2, -4, -2, 0, 0, -2, 0, 2, 2, -4, 2, 0],
     [0, -2, -2, 0, -2, 0, 4, 2, -2, 0, -4, 2, 0, -2, -2, 0],
     [0, 2, -2, 4, 2, 0, 0, 2, 0, -2, 2, 4, -2, 0, 0, -2],
     [0, -2, 0, 2, 2, -4, 2, 0, -2, 0, 2, 0, 4, 2, 0, 2],
     [0, 0, 0, 0, 0, 0, 0, 0, -2, 2, 2, -2, 2, -2, -2, -6],
     [0, 0, -2, -2, 0, 0, -2, -2, -4, 0, -2, 2, 0, 4, 2, -2],
     [0, 4, -2, 2, -4, 0, 2, -2, 2, 2, 0, 0, 2, 2, 0, 0],
     [0, 4, 0, -4, 4, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, -2, 4, -2, -2, 0, 2, 0, 2, 0, 2, 4, 0, 2, 0, -2],
     [0, 2, 2, 0, -2, 4, 0, 2, -4, -2, 2, 0, 2, 0, 0, 2],
     [0, 2, 2, 0, -2, -4, 0, 2, -2, 0, 0, -2, -4, 2, -2, 0],
     [0, -2, -4, -2, -2, 0, 2, 0, 0, -2, 4, -2, -2, 0, 2, 0]]


key = b'W\x88'
# last round key = b'ZN'

cipher = SPN(sbits=4, nblock=4, nround=4)

sbox_prim = [0xe, 4, 0xd, 1, 2, 0xf, 0xb, 8, 3, 0xa, 6, 0xc, 5, 9, 0, 7]
sbox = {int2bits(i, 4): int2bits(j, 4) for i, j in enumerate(sbox_prim)}

pbox = [0, 4, 8, 12, 1, 5, 9, 13, 2, 6, 10, 14, 3, 7, 11, 15]
random.shuffle(pbox)

cipher.set_boxes(sbox, pbox)
cipher.set_key(key)


# separate inputs of different sboxs
def group_by_sboxs(fins):
    ssboxs = {}

    for i in fins:
        boxid = i // 4
        mask = 1 << (3 - i % 4)
        if boxid not in ssboxs:
            ssboxs[boxid] = 0
        ssboxs[boxid] |= mask

    return ssboxs

def pat_to_pins(pat, base):
    l = int2bits(pat, 4)
    return [(base * 4 + i) for i, v in enumerate(l) if v == '1']

def find_paths(inputs, max_sboxs_span):
    full_paths = []

    def _dfs(level, fins, pbias):
        # print_ = functools.partial(print, ' ' * level * 2)
        def print_(*args, **kwargs):
            pass

        ssboxs = group_by_sboxs(fins)

        if level >= 3:
            if len(ssboxs) <= max_sboxs_span:
                print_('=>', fins, pbias)
                full_paths.append((fins, pbias))
            return

        print_('in', fins, ssboxs, 'bias', pbias)

        sbox_sels = []

        for boxid, pat_in in ssboxs.items():
            row = sbox_paths[pat_in]

            sbox_sels_cur = []
            sbox_sels.append(sbox_sels_cur)
            for pat_out, bias in enumerate(row):
                if abs(bias) < 4:
                    continue
                # do permutation
                outs = sorted(map(pbox.__getitem__, pat_to_pins(pat_out, boxid)))
                sbox_sels_cur.append((outs, bias / 16))

        print_('sbox selections:')
        pprint(sbox_sels, indent=level * 2 + 3)

        import itertools
        from operator import itemgetter
        from functools import reduce

        for sbox_sel in itertools.product(*sbox_sels):
            # the product may be empty but still yields a list
            if not sbox_sel:
                break

            # flatten and sort list
            sbox_comb = map(itemgetter(0), sbox_sel)
            biases = map(itemgetter(1), sbox_sel)

            # TODO: from heapq import merge
            combined = sorted(i for sl in sbox_comb for i in sl)
            bias_after = reduce(lambda x, y: x * y * 2, biases)
            _dfs(level + 1, combined, pbias * bias_after * 2)

        return

    # TODO: change prob. to logarithms if accu. is in concern
    _dfs(0, inputs, 0.5)

    return full_paths



def main():
    # paths = {}

    # for blk in range(4):
    #     for pat_in in range(16):
    #         fins = pat_to_pins(pat_in, blk)
    #         l = find_paths(fins, 2)

    #         for fouts, bias in l:
    #             kk = tuple(group_by_sboxs(fouts).keys())
    #             if kk not in paths:
    #                 paths[kk] = []
    #             paths[kk].append((fins, fouts, bias))

    # for sboxs_comb, path_list in paths.items():
    #     plist = sorted(path_list, key=lambda x: -abs(x[2]))
    #     print(sboxs_comb)
    #     pprint(plist[:15], indent=4)
    #     print()

    print('sbox =', cipher.sbox)
    print('pbox =', cipher.pbox)

    # for _ in range(10000):
    #     x = os.urandom(2)
    #     y = cipher.encrypt(x)
    #     print('x =', x.hex())
    #     print('y =', y.hex())


    print('keys =', list(map(lambda x: hex(int.from_bytes(x, 'big')), cipher.raw_keys)))
    # keys = ['0x8857', '0x5ab9', '0xb8c1', '0x3ef7', '0x4e5a']


if __name__ == '__main__':
    main()
