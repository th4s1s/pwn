from pwn import *

context.binary = exe = ELF('./warmup')
libc = ELF('./libc.so.6')

io = remote('34.76.152.107', 17012)

io.recvuntil(b'port ')
PORT = int(io.recvline(keepends=False))
io.recvuntil(b'?\n')

log.info(f'Port: {PORT}')
io.interactive()