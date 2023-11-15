from pwn import *

io = remote('188.166.220.129', 10001)

count = 1
while(1):
    try:
        io.recvuntil(b'> ')
    except:

    io.sendline(b'i'*i)