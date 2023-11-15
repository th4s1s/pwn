from pwn import *
import os

def solve_pow(conn):
    conn.recvuntil(b"proof of work: ")
    cmd = conn.recvline().decode().strip()
    log.info(cmd)
    sol = os.popen(cmd).read().strip()
    log.info(sol)
    conn.sendlineafter(b"solution: ", sol.encode())
    log.info("Done solving PoW.")

#One = 0xc9620

io = process('./noleek_patched')
gdb.attach(io, api=True)
io.interactive()
print(io.recvuntil(b'leek? '))
io.sendline(b'a')
print(io.recvuntil(b'leek? ', timeout=20))
io.sendline(b'a')
try:
    print(io.recvuntil(b'noleek.', timeout=20))
    io.sendline(b'cat flag.txt')
    print(io.recv(timeout=5))
except Exception as e:
    print("Error!")
io.close()