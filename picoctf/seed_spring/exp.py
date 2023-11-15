from pwn import *
from ctypes import CDLL

libc = CDLL('libc.so.6')

#io = process('./seed_spring')
libc.srand(libc.time(0))

while(1):
    io = remote('jupiter.challenges.picoctf.org', 35856)
    found = True
    for i in range(30):
        log.info(f'Hit number: {i+1}')
        io.recvuntil(b'height: ')
        io.sendline(str(libc.rand() & 0xf).encode())
        res = io.recvline()
        if b'WRONG!' in res:
            found = False
            io.close()
            break
    if found:
        break

io.interactive()
