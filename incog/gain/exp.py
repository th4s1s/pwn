from pwn import *

io = remote('143.198.219.171', 5003)

str0 = b'ICTF4'
str1 = b'dasDASQWgjtrkodsc'
str2 = p32(0xDEADBEEF)

print(io.recvuntil(b'Level 0:'))
io.sendline(str0)
print(io.recvuntil(b'Level 1:'))
io.sendline(str1)
print(io.recvuntil(b'Level 2:'))
io.sendline(str2)
io.interactive()