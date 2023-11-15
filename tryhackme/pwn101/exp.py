from pwn import *

io = remote('10.10.109.241', 9001)

io.interactive()