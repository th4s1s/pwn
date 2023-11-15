from pwn import *
from ctypes import CDLL

exe = ELF("./file_scanner")
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
    r = process('./local')
    r.interactive()
    test1 = r.recv(timeout=0.5).strip().split()
    print(test1)
    #test2 = bytes([int(i) for i in test1])
    #print(test2)

    io.recvuntil(b'ID: ')
    payload = b''
    io.send(payload)
    io.recvn()

    io.interactive()


if __name__ == "__main__":
    main()
