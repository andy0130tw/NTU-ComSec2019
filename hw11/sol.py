import random
import os
import math
import functools
import itertools
from pprint import pprint
import heapq
import copy
from spn import SPN, int2bits
import numpy as np
import ast
import hashlib


# random.seed(42)
nround = 4
# key = os.urandom(8)

with open('./output.txt') as f:
    sbox = ast.literal_eval(f.readline().split('=')[1].strip())
    pbox = ast.literal_eval(f.readline().split('=')[1].strip())

    lines = f.read().splitlines()
    enc = bytes.fromhex(lines.pop()[6:])

cipher = SPN(sbits=4, nblock=16, nround=nround)
cipher.set_boxes(sbox, pbox)

sbits, nbits = cipher.sbits, cipher.nbits
N = 1 << sbits


# above is from OCR-ed lab11-2


# THIS LINE IS DUMB BUT REQUIRED
import __utils
from __utils import *
from operator import itemgetter
from multiprocessing import (Pool, Event, Process, Array)


def partial_decrypt(y):
    ks = iter(round_keys_inv)

    for k in ks:
        y = cipher.add_round_key(y, k)
        y = cipher.substitute(y, cipher.isbox)
        y = cipher.permute(y, cipher.ipbox)

        if i != nround - 1:
            y = cipher.permute(y, cipher.ipbox)

    # if nround == 0:
    #     print('the key is', int(cipher.add_round_key(x, y), 2).to_bytes(nbits // 8, 'little'))

    return y

nblock = cipher.nblock

round_keys_inv = list(
    map(lambda x: int2bits(x, nbits), [
        # placeholders...
        # 0x4dbf_cb9c_3d81_ff1b,
        # 0x0000_0000_0000_0000,
        # 0x1111_1111_1111_1111,
        # 0x2222_2222_2222_2222,
        # 0x3333_3333_3333_3333,
    ]))

is_revealing_last_round = False
nlevels = 3

assert (nlevels == nround - 1) == (is_revealing_last_round)
assert len(round_keys_inv) + nlevels == nround - 1


data = []
for x, y in zip(lines[::2], lines[1::2]):
    x = transform_input_hex(x[4:], nbits)
    y = transform_input_hex(y[4:], nbits)
    y = partial_decrypt(y)
    data.append((x, y))

# data = data[:1000]

linear_approx_table = (
[[8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
 [0, 4, -2, 2, -4, 0, 2, -2, 0, 0, 2, 2, 0, 0, 2, 2],
 [0, 0, -2, 2, 2, 2, 4, 0, -2, 2, 0, 0, 0, 4, -2, -2],
 [0, -4, 0, 0, -2, 2, 2, 2, 2, -2, 2, 2, 4, 0, 0, 0],
 [0, 0, 0, -4, -4, 0, 0, 0, -2, 2, -2, -2, 2, 2, -2, 2],
 [0, 0, -2, 2, 0, -4, 2, 2, -2, -2, 0, -4, 2, -2, 0, 0],
 [0, 0, -2, -2, 2, -2, 0, -4, 0, 0, 2, 2, 2, -2, -4, 0],
 [0, 0, 0, 0, -2, 2, -2, 2, -4, 0, 4, 0, -2, -2, -2, -2],
 [0, 2, -4, -2, 0, 2, 0, 2, 0, -2, -4, 2, 0, -2, 0, -2],
 [0, -2, -2, -4, 0, -2, 2, 0, 0, -2, 2, 0, -4, 2, 2, 0],
 [0, 2, 2, 0, -2, 0, 0, -2, 2, -4, 0, -2, 0, 2, -2, -4],
 [0, -2, 0, 2, -2, -4, -2, 0, -2, 0, -2, 4, 0, 2, 0, -2],
 [0, 2, 0, -2, 0, -2, 0, 2, 2, 4, 2, 0, 2, 0, 2, -4],
 [0, 2, 2, 0, 0, -2, 2, 4, 2, 0, 0, 2, -2, 0, -4, 2],
 [0, 2, -2, 0, 2, 0, -4, 2, 0, -2, 2, 0, 2, 4, 0, 2],
 [0, 2, 4, -2, 2, 0, 2, 0, -4, -2, 0, 2, 2, 0, 2, 0]])


def find_paths(latable, inputs):
    full_paths = []

    def _dfs(level, fins, pbias):
        def print_(*args, **kwargs):
            return
            print(' ' * level * 4, end='')
            print(*args, **kwargs)

        ssboxs = group_by_sboxs(fins)

        if level >= nlevels:
            if abs(pbias) > 0.01:
                print_('=>', fins, pbias)
                full_paths.append((fins, pbias))
            return

        print_('DFS in', fins, ssboxs, 'bias', pbias)

        sbox_sels = []

        for boxid, pat_in in ssboxs.items():
            # pick a biased substitution for each active S-box
            row = latable[pat_in]

            sbox_sels_cur = []
            sbox_sels.append(sbox_sels_cur)
            for pat_out, bias in enumerate(row):
                if abs(bias) < 4:
                    continue
                # do permutation
                outs = sorted(map(cipher.ipbox.__getitem__, pat_to_pins(pat_out, boxid)))
                sbox_sels_cur.append((outs, bias / N))

        print_('sbox selections:')
        for sel in sbox_sels:
            print_('  * %r' % sel)

        for sbox_sel in itertools.product(*sbox_sels):
            # the product may be empty but still yields a list
            if not sbox_sel:
                break

            # flatten and sort list
            # pats_sel = map(itemgetter(0), sbox_sel)
            sbox_comb = map(itemgetter(0), sbox_sel)
            biases = map(itemgetter(1), sbox_sel)

            # TODO: from heapq import merge
            combined = sorted(i for sl in sbox_comb for i in sl)
            bias_total = functools.reduce(lambda x, y: x * y * 2, biases)
            _dfs(level + 1, combined, pbias * bias_total * 2) #tuple(pats_sel)

        return


    # TODO: change prob. to logarithms if accu. is in concern
    _dfs(0, inputs, 0.5)

    return full_paths


def path_gen():
    pats_seen_count = 0

    # all_patterns = (
    #     list(itertools.product([(i,) for i in range(nblock)], range(1, N))) +
    #     list(itertools.product(range_triangle(nblock), range(1, N))))
    # print(len(all_patterns))
    # random.shuffle(all_patterns)
    sbox_comb_double = range_triangle(nblock)
    random.shuffle(sbox_comb_double)

    for blks in list((i,) for i in range(nblock)) + sbox_comb_double:

        pats_prod = itertools.product(*([range(1, N)] * len(blks)))

        for pats in pats_prod:
            fins = sum([pat_to_pins(pat, blk) for pat, blk in zip(pats, blks)], [])
            plist_raw = find_paths(linear_approx_table, fins)

            plist = plist_raw
            plist = [(fins, *p) for p in plist]
            plist = sorted(plist, key=lambda x: abs(x[2]), reverse=True)[:2]

            if plist:
                print(f'#{pats_seen_count:5d}: Generated {len(plist)} paths')
                pprint(plist)

            yield from plist

            pats_seen_count += 1


# from array import array

def simulate(path_spec):
    counters_single = __utils.counters_single

    fins, fouts, bias = path_spec

    sboxs_o_pats = group_by_sboxs(fouts)
    output_sboxs = sboxs_o_pats.items()

    sboxs_a_pats = sboxs_o_pats
    affected_sboxs = output_sboxs


    if len(affected_sboxs) > 2:
        return

    print('Simulating', fins, '->', fouts,
          'affecting sbox', ','.join(map(str, sboxs_a_pats.keys())),
          'bias', bias)

    # itertools.product(*[range(16) for _ in affected_sboxs])
    for target_subkeys in itertools.product(*[range(N) for _ in affected_sboxs]):
        cnt = 0

        for xx, yy in data:
            xored = 0

            # xor fan-ins
            for i in fins:
                xored ^= int(xx[i], 2)

            # construct masked key

            blocked_key = ['0' * sbits] * nblock
            for (blkid, _), subkey in zip(affected_sboxs, target_subkeys):
                blocked_key[blkid] = int2bits(subkey, sbits)

            key = ''.join(blocked_key)

            # if not is_revealing_last_round:
            #     key = cipher.substitute(key, cipher.sbox)

            # partial decrypts affected sboxs
            yy_rev = yy
            #   add round key
            yy_rev = cipher.add_round_key(yy_rev, key)
            #   inverse S-box
            yy_rev = cipher.substitute(yy_rev, cipher.isbox)

            for (blkid, pat) in output_sboxs:
                blk_base = blkid * sbits

                blk_rev = yy_rev[blk_base:(blk_base + sbits)]

                # xor fan-outs
                for offs, bit in enumerate(int2bits(pat, sbits)):
                    if int(bit, 2):
                        xored ^= int(blk_rev[offs], 2)

            # (0, 1) -> (-1, 1)
            cnt += ((xored << 1) - 1)

        # makes biases add-able by converting them positive

        if len(affected_sboxs) == 1:
            ia, = sboxs_a_pats.keys()
            ka, = target_subkeys
            counters_single[ia][ka] += abs(cnt)
            # cand_single[ia].increment(ka, abs(cnt))

        elif len(affected_sboxs) == 2:
            ia, ib = sboxs_a_pats.keys()
            ka, kb = target_subkeys
            counters_single[ia][ka] += abs(cnt)
            counters_single[ib][kb] += abs(cnt)
            # __utils.counters_double[(ia, ib)].increment((ka << 4) + kb, abs(cnt))
            # cand_single[ia].increment(ka, abs(cnt))
            # cand_single[ib].increment(kb, abs(cnt))

        else:
            break


def pool_init(cand_single):
    __utils.counters_single = cand_single


def report(cand_single):
    most_probable = []

    for i in range(nblock):
        top_cands = sorted(enumerate(cand_single[i]), key=lambda x: abs(x[1]))[::-1][:5]
        # color_str = '\033[01;33m' if i in sboxs_pats else '\033[01m'
        color_str = '\033[01;33m' if 0 else '\033[01m'
        print(f'{color_str}#{i:2d}\033[0m:   ', end='')

        if not top_cands or top_cands[0][1] == 0:
            print('N/A')
            continue
        else:
            best_cand, _ = top_cands[0]
            most_probable.append(int2bits(best_cand, sbits))

        for char, cnt in top_cands:
            print(f'[\033[01;34m{hex(char)[2:]}\033[0m {cnt:6d}]   ', end='')
        print()

    if not is_revealing_last_round and len(most_probable) == nblock:
        result = ''.join(most_probable)
        result = cipher.permute(result, cipher.pbox)
        result = hex(int(result, 2))[2:]

        print(f'Most probable result: \033[01;32m{result}\033[01;0m')


def main():
    if nround == -1:
        enc = bytes.fromhex(enc)
        key = round_keys_inv[-1]
        k = hashlib.sha512(key).digest()
        flag = bytes(ci ^ ki for ci, ki in zip(enc, k))
        print(flag)
    else:
        # cand_single = {k: Counter() for k in range(16)}
        cand_single = [Array('l', N) for _ in range(nblock)]
        # cand_double = {k: Counter() for k in range_triangle(16)}

        with Pool(processes=16, initializer=pool_init, initargs=(cand_single,)) as pool:
            g = path_gen()

            pcg = pool.imap_unordered(simulate, g, 5)

            x = 0

            for _ in pcg:
                x += 1
                if x % 80 != 0: continue

                report(cand_single)

if __name__ == '__main__':
    main()
