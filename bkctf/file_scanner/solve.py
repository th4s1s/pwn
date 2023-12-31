#!/usr/bin/env python3

from pwn import *

exe = ELF("./file_scanner_patched")
libc = ELF("./libc_32.so.6")
ld = ELF("./ld-2.23.so")

context.binary = exe


def conn():
    if args.LOCAL:
        r = process([exe.path])
        if args.DEBUG:
            gdb.attach(r)
    else:
        r = remote("addr", 1337)

    return r


def main():
    io = conn()

    # good luck pwning :)

    io.interactive()


if __name__ == "__main__":
    main()
