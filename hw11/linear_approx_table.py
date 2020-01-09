import sys
from pprint import pprint

# sbox from the tutorial
# sbox = [0xe, 4, 0xd, 1, 2, 0xf, 0xb, 8, 3, 0xa, 6, 0xc, 5, 9, 0, 7]
sbox = [0xe, 0x2, 0x6, 0xd, 0x7, 0x8, 0xa, 0x3, 0xf, 0x9, 0xc, 0x5, 0x0, 0xb, 0x4, 0x1]
SIZE_SBOX = len(sbox)

# compute the linear approximation for a given "input = output" equation
def linearApprox(input_int, output_int):
    total = 0
    # range over the input
    for ii in range(SIZE_SBOX):
        # get input and output of our equations
        input_masked = ii & input_int
        output_masked = sbox[ii] & output_int
        # same result?
        if (bin(input_masked).count("1") - bin(output_masked).count("1")) % 2 == 0:
            total += 1
    # get the number of results compared to 8/16
    result = total - (SIZE_SBOX//2)
    return result

def main():
    # rows
    # sys.stdout.write( "    | ")
    # for i in range(SIZE_SBOX):
    #     sys.stdout.write(hex(i)[2:].rjust(3) + " ")
    # print ("")
    # print (" " + "-" * (SIZE_SBOX * 4 + 4))

    buf = []

    for row in range(SIZE_SBOX):
        # sys.stdout.write(hex(row)[2:].rjust(3) +  " | ")
        ln = []
        buf.append(ln)
        for col in range(SIZE_SBOX):
            # print the linear approx
            bias = linearApprox(row, col)
            ln.append(bias)

        # print ("")

    pprint(buf)

if __name__ == "__main__":
    main()

'''
    |   0   1   2   3   4   5   6   7   8   9   a   b   c   d   e   f
 --------------------------------------------------------------------
  0 |  +8   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0
  1 |   0  +4  -2  +2  -4   0  +2  -2   0   0  +2  +2   0   0  +2  +2
  2 |   0   0  -2  +2  +2  +2  +4   0  -2  +2   0   0   0  +4  -2  -2
  3 |   0  -4   0   0  -2  +2  +2  +2  +2  -2  +2  +2  +4   0   0   0
  4 |   0   0   0  -4  -4   0   0   0  -2  +2  -2  -2  +2  +2  -2  +2
  5 |   0   0  -2  +2   0  -4  +2  +2  -2  -2   0  -4  +2  -2   0   0
  6 |   0   0  -2  -2  +2  -2   0  -4   0   0  +2  +2  +2  -2  -4   0
  7 |   0   0   0   0  -2  +2  -2  +2  -4   0  +4   0  -2  -2  -2  -2
  8 |   0  +2  -4  -2   0  +2   0  +2   0  -2  -4  +2   0  -2   0  -2
  9 |   0  -2  -2  -4   0  -2  +2   0   0  -2  +2   0  -4  +2  +2   0
  a |   0  +2  +2   0  -2   0   0  -2  +2  -4   0  -2   0  +2  -2  -4
  b |   0  -2   0  +2  -2  -4  -2   0  -2   0  -2  +4   0  +2   0  -2
  c |   0  +2   0  -2   0  -2   0  +2  +2  +4  +2   0  +2   0  +2  -4
  d |   0  +2  +2   0   0  -2  +2  +4  +2   0   0  +2  -2   0  -4  +2
  e |   0  +2  -2   0  +2   0  -4  +2   0  -2  +2   0  +2  +4   0  +2
  f |   0  +2  +4  -2  +2   0  +2   0  -4  -2   0  +2  +2   0  +2   0
'''
