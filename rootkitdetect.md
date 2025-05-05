# Cheatsheet

[TOC]

## Rootkits

Other sources:
 + [Cheat sheet for detect and remove linux kernel rootkits](https://github.com/MatheuZSecurity/detect-lkm-rootkit-cheatsheet)
 + [The Art of Rootkits](https://inferi.club/post/the-art-of-linux-kernel-rootkits)

### Preventive measures

Disable ftrace:
```bash
sysctl -w kernel.ftrace_enabled=1
```

### Detection

#### Oracle
If this command prints sth to stdout it means that there is potentially a rootkit installed on the system.
Tested with:
 + [Diamorphine](https://github.com/m0nad/Diamorphine)
 + [KoviD](https://github.com/carloslack/KoviD/tree/master)
```bash
grep -a \
  "\[$( \
      comm -23 \
        <(perl -nE 'say $1 if /\[(.*)\]/' /proc/kallsyms | grep -v '^bpf$' | sort | uniq) \
        <(lsmod | awk '{print $1}' | sort) \
   )\]" \
   /proc/kallsyms 
```
Note: After the rootkit has been removed, the above command will still print sth to stdout:
```
0000000000000000 t ftrace_trampoline    [__builtin__ftrace]
```

#### Diamorphine
if the [Oracle](#oracle) script outputs sth like this:
```
0000000000000000 T diamorphine_init     [diamorphine]
0000000000000000 t ftrace_trampoline    [__builtin__ftrace]
```

#### KoviD
if the [Oracle](#oracle) script outputs sth like this:
```
0000000000000000 t ftrace_trampoline    [__builtin__ftrace]
0000000000000000 t ftrace_trampoline    [__builtin__ftrace]
0000000000000000 t ftrace_trampoline    [__builtin__ftrace]
0000000000000000 t ftrace_trampoline    [__builtin__ftrace]
0000000000000000 t ftrace_trampoline    [__builtin__ftrace]
0000000000000000 t ftrace_trampoline    [__builtin__ftrace]
0000000000000000 t ftrace_trampoline    [__builtin__ftrace]
0000000000000000 t ftrace_trampoline    [__builtin__ftrace]
0000000000000000 t ftrace_trampoline    [__builtin__ftrace]
0000000000000000 t ftrace_trampoline    [__builtin__ftrace]
0000000000000000 t ftrace_trampoline    [__builtin__ftrace]
0000000000000000 t ftrace_trampoline    [__builtin__ftrace]
0000000000000000 t ftrace_trampoline    [__builtin__ftrace]
0000000000000000 t ftrace_trampoline    [__builtin__ftrace]
0000000000000000 t ftrace_trampoline    [__builtin__ftrace]
0000000000000000 t ftrace_trampoline    [__builtin__ftrace]
0000000000000000 t ftrace_trampoline    [__builtin__ftrace]
0000000000000000 t ftrace_trampoline    [__builtin__ftrace]
0000000000000000 t ftrace_trampoline    [__builtin__ftrace]
0000000000000000 t ftrace_trampoline    [__builtin__ftrace]
0000000000000000 t ftrace_trampoline    [__builtin__ftrace]
0000000000000000 t ftrace_trampoline    [__builtin__ftrace]
```

### Removal

#### Diamorphine

Use [ModTracer](https://github.com/MatheuZSecurity/ModTracer/tree/main) to make Diamorphine visiable. \
Then you can unload the module.
```bash 
git clone https://github.com/MatheuZSecurity/ModTracer
cd ModTracer
make
sudo insmod modtracer.ko
# check dmesg if a rootkit was found, if diamorphine was found remove it
rmmod diamorphine
```

#### KoviD
best bet is to just reload the kernel (`reboot`). \ 
it is also important to find the perstistence mechanism and remove it. \ 
check `cat /var/.kv.ko` (note: this file wont be listable, but you can read it)
