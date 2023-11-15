from pwn import *

r = remote("saturn.picoctf.net", 56981)

play = b"1\n" + b"rock/paper/scissors\n"
r.sendline(play)
r.sendline(play)
r.sendline(play)
r.sendline(play)
r.sendline(play)

r.interactive()