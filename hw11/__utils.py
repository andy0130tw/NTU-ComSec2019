import itertools

from spn import int2bits


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

def pins_to_int(lst):
    x = 0
    for b in lst:
        x |= (1 << b)
    return x

def transform_input_hex(x, nbits):
    x = bytes.fromhex(x)
    x = int.from_bytes(x, 'little')
    x = int2bits(x, nbits)
    return x


range_triangle = lambda n: [(i, j) for i, j in itertools.product(range(n), range(n)) if i < j]
