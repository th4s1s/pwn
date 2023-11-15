from pwn import *

r = remote("thekidofarcrania.com", 10001)

# payload = b"1000000"
# r.sendline(payload)
# r.sendline(payload)

r.interactive()