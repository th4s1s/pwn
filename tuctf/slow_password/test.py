from pwn import *
r = remote("chals.tuctf.com", 30200)
res = r.recvlineS()

while 1 < 2:
    d = eval(res)
    d = str(d)
    r.sendline(d)
    res = r.recvlineS()
    if "TUCTF" in res:
        break
    elif "Incorrect!" in res:
        break