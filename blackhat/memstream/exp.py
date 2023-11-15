from pwn import *

context.binary = exe = ELF('./memstream')

io = process()
gdb.attach(io, api=True)

io.interactive()
io.sendlineafter(b'> ', b'3')
io.sendlineafter(b': ', b'100')
io.sendlineafter(b': ', b'a\0')