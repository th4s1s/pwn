from pwn import *
r = remote("chals.tuctf.com", 30202)

while 1 < 2:
    res = r.recvlineS()
    d = eval(res)
    d = str(d)
    r.sendline(d)
    res = r.recvlineS()
    print(res)
    if "TUCTF" in res:
        break
    elif "Incorrect!" in res:
        break