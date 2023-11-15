from pwn import *
for i in range(1712, 2048):
    io = remote('jupiter.challenges.picoctf.org', 44628)
    log.info(f'Trying {i}')
    io.recvuntil(b'?\n')
    io.sendline(str(i).encode())

    res = io.recvline()
    if b'Nope!' not in res:
        break
    io.close()
