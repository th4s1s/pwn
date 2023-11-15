from pwn import *

context.binary = exe = ELF('./chall')
libc = ELF('./libc.so.6')

io = process()
gdb.attach(io, api=True)

io.recvuntil(b'> ')
io.sendline(b'2')

io.recvuntil(b'index: ')
io.sendline(b'9')

io.recvuntil(b'data: ')
io.send(b'a')

io.interactive()