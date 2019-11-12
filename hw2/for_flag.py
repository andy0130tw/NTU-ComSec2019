
'''
0x404058 transformed code

undefined4 UndefinedFunction_00404058(int param_1,int param_2)

{
  int iStack8;

  iStack8 = 0;
  while( true ) {
    if (*(char *)(param_2 + iStack8) == '\0') {
      return 1;
    }
    if ((byte)(*(char *)(param_1 + iStack8) + 0x23U ^ 0x66) != *(byte *)(param_2 + iStack8)) break;
    iStack8 = iStack8 + 1;
  }
  return 0;
}
'''

data4018 = '0f 09 31 0c f8 14 ed 36 fa ee e2 ed 36 1e 36 0c 35 3c 36 3c ed 30 36 ef 31 e8 ee ef e9 e2 ec c6 00 00 d1 00 00 e6 43 ba 28 34 18 43 ba 04 ec ee fb b4 ec e6 48 bd ae 07 c9 fc fe 46 f8 40 36 00'

conv = lambda s: bytes([int(x, 16) for x in s.split(' ')])

sec1 = conv(data4018)

sec1_real = [i for i in sec1]

for i in range(32):
    sec1_real[i] = (sec1[i] + sec1[i+32]) & 0xff

sec1_real = bytes(sec1_real)
print(sec1_real)

print(''.join([chr(((sec1_real[i]^0x66) + 256 - 0x23) % 256) for i in range(64)]))
