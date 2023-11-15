from pwn import *

context.binary = exe = ELF('./warmup')
libc = ELF('./libc.so.6')

io = process()
gdb.attach(io, api=True)

io.interactive()