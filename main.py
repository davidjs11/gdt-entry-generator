# --- useful functions ---
def bool_input(message):
    while True:
        user_input = input(message).strip().lower()
        if user_input in ['yes', 'y', 'true', 't', '1']:
            return True
        elif user_input in ['no', 'n', 'false', 'f', '0']:
            return False
        else:
            print("input not valid.")

def range_input(message, lower, upper, base=10):
    while True:
        user_input = int(input(message), base)
        if user_input not in range(lower, upper+1):
            if base==2:
                print(f"error: option not in range (0b{lower:b}, \
                        0b{upper:b})")
            if base==10:
                print(f"error: option not in range ({lower}, {upper})")
            if base==16:
                print(f"error: option not in range (0x{lower:X}, \
                        0x{upper:X})")
        else: 
            return user_input


if __name__ == "__main__":
    # type (code/data/ldt/tss)
    print("0 - data segment")
    print("1 - code segment")
    # print("2 - LDT segment") # not available atm
    # print("3 - TSS segment")
    seg_type = range_input("segment type: ", 0, 1)

    # 64-bit?
    _64bit = bool_input("is the system 64-bits? (Y/N): ")
    if _64bit:
        print("not supported yet :-(")
        exit(-1)
    max_addr = pow(2, 32 + 32*_64bit)-1

    # data segment
    if seg_type == 0:
        write = bool_input("can the segment be written? (Y/N): ")

    # code segment
    if seg_type == 1:
        read = bool_input("can the segment be read? (Y/N): ")
        conforming = bool_input("conforming segment? (Y/N): ")

    # base address
    base = range_input(f"base address (0x0, 0x{max_addr:X}): ",\
                       0, max_addr, 16)

    # granularity
    granularity = bool_input("granularity (0: 1B - 1: 4KB): ")
    if granularity:
        max_size = int(((max_addr-base+1)/pow(2, 12))-1)
    else:
        max_size = min(int(max_addr-base+1), 0xFFFFF)

    # limit (size - 1)
    limit = range_input(f"segment limit (hex) (0x1, 0x{max_size:X}): ",\
                        1, max_size, 16)

    # privilege level
    privilege = range_input("privilege level (0-3): ", 0, 3)


    # --- create gdt entry ---
    gdt_entry  = f"{base:032b}"[0:8]            # base addr 31:24
    gdt_entry += "1" if granularity else "0"    # granularity
    gdt_entry += "1"                            # d/b
    gdt_entry += "1" if _64bit else "0"         # 64-bit code seg.
    gdt_entry += "0"                            # available/free
    gdt_entry += f"{limit:020b}"[0:4]           # limit 19:16
    gdt_entry += "1"                            # present flag
    gdt_entry += f"{privilege:02b}"             # privilege level
    gdt_entry += "1"                            # type (only code/data atm)

    # data segment
    if seg_type == 0:
        gdt_entry += "0"                        # data
        gdt_entry += "0"                        # expand-down (not available)
        gdt_entry += "1" if write else "0"      # write
        gdt_entry += "0"                        # accessed

    # code segment
    if seg_type == 1:
        gdt_entry += "1"                        # code
        gdt_entry += "1" if conforming else "0" # conforming
        gdt_entry += "1" if read else "0"       # read
        gdt_entry += "0"                        # accessed

    gdt_entry += f"{base:032b}"[8:16]           # base addr 23:16
    gdt_entry += f"{base:032b}"[16:]            # base addr 15:00
    gdt_entry += f"{limit:020b}"[4:]            # limit 15:00


    # --- result ---
    print()
    print(f"gdt entry:")
    print(f"bin: 0b{gdt_entry}")
    print(f"hex: 0x{int(gdt_entry, 2):X}")

# the end!
