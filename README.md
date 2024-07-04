## GDT entry generator

A basic script that creates a GDT entry by using user input.

#### Current progress:
- [x] Support for 32-bit protected mode.
- [ ] Support for 64-bit long mode.
- [ ] System segment entries (TSS, LDT...).

#### Use example:
```
$ python main.py
   0 - data segment
   1 - code segment
   segment type: 0
   is the system 64-bits? (Y/N): n
   can the segment be written? (Y/N): y
   base address (0x0, 0xFFFFFFFF): 0  
   granularity (0: 1B - 1: 4KB): 1
   segment limit (hex) (0x1, 0xFFFFF): FFFFF
   privilege level (0-3): 0

   gdt entry:
   bin: 0b0000000011001111100100100000000000000000000000001111111111111111
   hex: 0xCF92000000FFFF
```

It is recommended to read Volume 3A, Chapter 3 from Intel SDM, which can be found at https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html
