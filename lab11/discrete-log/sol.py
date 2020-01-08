import ast
import math
from tqdm import tqdm, trange
from fact import factors
import hashlib
import libnum


# Loading data
with open('./output.txt') as f:
    g = ast.literal_eval(f.readline()[4:])
    n = ast.literal_eval(f.readline()[4:])
    c = ast.literal_eval(f.readline()[4:])
    enc = bytes.fromhex(f.readline()[7:])

# Sanity check
z = 1
for f in factors:
    z *= f
assert z == n - 1


# Pohlih-hellman
# Solve in subgroups
remainders = []
for f in tqdm(factors):
    # Raising to subgroup
    m = (n - 1) // f
    sqf = math.ceil(math.sqrt(f))
    gf = pow(g, m, n)
    gsqf = pow(gf, sqf, n)

    table = {}

    # Giant step
    ygna = pow(c, m, n)
    for a in trange(sqf, leave=False):
        table[ygna] = a
        ygna = (ygna * gsqf) % n

    # Baby step
    gb = 1
    for b in trange(sqf, leave=False):
        if gb in table:
            a = table[gb]
            # gf^b = cy^a = gf^(ki + a * sqf)
            ki = (b - a * sqf) % f
            remainders.append(ki)
            break
        gb = (gb * gf) % n


# Reconstruct
k = libnum.solve_crt(remainders, factors)


# Print flag
k = hashlib.sha512(str(k).encode('ascii')).digest()
dec = bytes(ci ^ ki for ci, ki in zip(enc, k))
print(dec)
