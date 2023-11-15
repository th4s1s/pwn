from pwn import *

io = remote('blackjack.misc.ctf.umasscybersec.org', 2207)
io.recvuntil(b'"ready"\n')
io.sendline(b'ready')
for i in range(10000):
    log.info('Round {}:'.format(i+1))
    io.recvuntil(b')\n')
    io.sendline(b'stand')
io.interactive()