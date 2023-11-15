from pwn import *

r = remote("thekidofarcrania.com", 4902)
pad = b'a'*60
shell = b'/sh\0'


r.interactive()