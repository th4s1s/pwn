from pwn import *

context.binary = exe = ELF('./chall')

io = process()

for i in range(100):
    io.recvuntil(b'> ')
    io.sendline(b'1')
    io.recvuntil(b'is ')
    addr = io.recvline(keepends=False).decode()
    log.info(f'Note {i}: {addr}')