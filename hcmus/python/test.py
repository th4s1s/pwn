#!/usr/bin/env python3

from ctypes import CDLL, c_buffer
libc = CDLL('/lib/x86_64-linux-gnu/libc.so.6')
buf1 = c_buffer(50)
buf2 = c_buffer(50)
libc.gets(buf1)
libc.puts(buf1)
libc.puts(buf2)
if b'HCMUS-CTF' in bytes(buf2):
    print(open('./flag.txt', 'r').read())
