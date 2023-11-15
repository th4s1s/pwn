from pwn import *
io = process('./chal')
exe = ELF('./chal')
gdb.attach(io, api=True)
print(hex(exe.got['exit']))
io.interactive()