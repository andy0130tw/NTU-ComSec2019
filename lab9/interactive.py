import binascii
import string

def xor(a, b):
    return b''.join(map(lambda x: chr(x[0] ^ x[1]).encode(), zip(a, b)))


with open('ciphers') as f:
    ciphers = [binascii.unhexlify(ln.strip()) for ln in f]

n = len(ciphers)
L = len(ciphers[0])

print(n)

prefix = b'FLAG{D0_u_know_One-Time-Pad\'s_md5_i5_37d52ab882a1397bec4e3e4eafba0f58??!!?!?'
key = prefix + b'\0' * (L-len(prefix)-1) + b'}'

allowed_characters = string.ascii_letters + ' ,.!?-()'
# allowed_characters = list(map(chr, range(32, 128)))

for cipher in ciphers:
    plain = xor(key, cipher)
    for k in range(L):
        print(chr(plain[k]) if key[k] else '|', end='')
    print()

for k in range(L):
    if key[k] != 0:
        continue
    cand = ''
    for c in range(32, 128):
        for cipher in ciphers:
            if chr(cipher[k] ^ c) not in allowed_characters:
                break
        else:
            cand += chr(c)
    print('[%2d]: %s' % (k, cand))
