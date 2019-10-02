
conv = lambda s: bytes([int(x, 16) for x in s.split(' ')])

fullyear = 1985
fullyear_8 = (fullyear % 256 + 63) * 2

assert fullyear_8 % 256 == 0

# @ 0x408008
guard = conv('1d 13 10 18 51 4c 4f 1c 12 51 0b 08 50 51 50 51 50 51 50 00')
# @ 0x40801c
key = conv('5b 5f 51 5f 2a 1c 0a 43 33 02 54 4d 11 02 09 2c 70 71 70 00')

print(''.join([chr(i ^ j) for i, j in zip(guard, key)]))
