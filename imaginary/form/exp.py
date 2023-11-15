from pwn import *

io = process('./vuln')
gdb.attach(io, api=True)

io.interactive()