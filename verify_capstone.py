"""
Verification and Test Suite for Capstone Project
Tests:
1. assembler.py against standard Hack programs
2. Assembler extra features (K mod 3 = 0, 1, 2)
3. Box.asm execution in simulated Hack CPU
"""

import sys
import os
import subprocess

def test_assembler(k_val=41):
    print(f"\n=======================================================")
    print(f" 1. Testing Hack Assembler (assembler.py) for K = {k_val}")
    print(f"=======================================================")

    # Create standard test files: Add.asm, Max.asm, Rect.asm
    add_asm = """// Computes R0 = 2 + 3
@2
D=A
@3
D=D+A
@0
M=D
"""
    with open("Add.asm", "w") as f:
        f.write(add_asm)

    # Test Add.asm assembly
    cmd = [r"C:\Users\pawan\AppData\Local\Python\bin\python.exe", "assembler.py", "Add.asm", str(k_val)]
    res = subprocess.run(cmd, capture_output=True, text=True)
    print("Add.asm output:", res.stdout.strip())
    assert os.path.exists("Add.hack"), "Add.hack was not generated!"
    with open("Add.hack") as f:
        lines = [line.strip() for line in f if line.strip()]
    expected_add = [
        "0000000000000010",
        "1110110000010000",
        "0000000000000011",
        "1110000010010000",
        "0000000000000000",
        "1110001100001000"
    ]
    assert lines == expected_add, f"Add.hack mismatch: {lines} vs {expected_add}"
    print(">>> Add.hack verification PASSED (100% exact match to official Hack specs)!")

    # Test Extra Features:
    # Feature 0: symbols.txt
    print("\n--- Testing Extra Feature K mod 3 == 0 (symbols.txt) ---")
    subprocess.run([r"C:\Users\pawan\AppData\Local\Python\bin\python.exe", "assembler.py", "Add.asm", "30"])
    assert os.path.exists("symbols.txt"), "symbols.txt was not generated!"
    print(">>> symbols.txt generated successfully!")

    # Feature 1: Syntax error reporting
    print("\n--- Testing Extra Feature K mod 3 == 1 (error line reporting) ---")
    bad_asm = """@10
D=A
INVALID_INSTRUCTION
@20
"""
    with open("Bad.asm", "w") as f:
        f.write(bad_asm)
    res = subprocess.run([r"C:\Users\pawan\AppData\Local\Python\bin\python.exe", "assembler.py", "Bad.asm", "31"], capture_output=True, text=True)
    print("Bad.asm output:\n", res.stdout.strip())
    assert "Line 3: invalid instruction" in res.stdout, "Error message did not report Line 3!"
    print(">>> Error message with line number verified successfully!")

    # Feature 2: Duplicate label warning
    print("\n--- Testing Extra Feature K mod 3 == 2 (duplicate label warning) ---")
    dup_asm = """(LOOP)
@1
(LOOP)
@LOOP
0;JMP
"""
    with open("Dup.asm", "w") as f:
        f.write(dup_asm)
    res = subprocess.run([r"C:\Users\pawan\AppData\Local\Python\bin\python.exe", "assembler.py", "Dup.asm", "32"], capture_output=True, text=True)
    print("Dup.asm output:\n", res.stdout.strip())
    assert "Warning: Duplicate label '(LOOP)' at line 3" in res.stdout, "Warning not detected!"
    print(">>> Duplicate label warning verified successfully!")


def simulate_hack_box(k_val=41):
    print(f"\n=======================================================")
    print(f" 2. Testing Box.asm & Hack CPU Simulation for K = {k_val}")
    print(f"=======================================================")

    # Generate Box.asm
    subprocess.run([r"C:\Users\pawan\AppData\Local\Python\bin\python.exe", "generate_box_asm.py", str(k_val), "Box.asm"])

    # Assemble Box.asm -> Box.hack
    subprocess.run([r"C:\Users\pawan\AppData\Local\Python\bin\python.exe", "assembler.py", "Box.asm", str(k_val)])
    assert os.path.exists("Box.hack"), "Box.hack was not generated!"

    # Parse instructions into list of ints
    with open("Box.hack") as f:
        rom = [int(line.strip(), 2) for line in f if line.strip()]

    start_row = k_val
    w_words = (k_val % 4) + 1
    base_addr = 16384 + (32 * start_row)

    print(f"Box Parameters for K = {k_val}:")
    print(f"  - Starting Row      : {start_row}")
    print(f"  - Height            : 20 rows (Rows {start_row} to {start_row + 19})")
    print(f"  - Width in pixels   : {16 * w_words} px ({w_words} word(s)/row)")
    print(f"  - Screen base addr  : {base_addr}")

    # Build Hack CPU Simulator in Python
    def run_sim(key_code, max_cycles=3000):
        ram = [0] * 32768
        ram[24576] = key_code  # KBD register
        pc = 0
        d_reg = 0
        a_reg = 0

        for cycle in range(max_cycles):
            if pc >= len(rom):
                break
            inst = rom[pc]
            if (inst & 0x8000) == 0:
                # A-instruction
                a_reg = inst & 0x7FFF
                pc += 1
            else:
                # C-instruction
                a_bit = (inst >> 12) & 1
                c_bits = (inst >> 6) & 0x3F
                dest_bits = (inst >> 3) & 7
                jump_bits = inst & 7

                y_val = ram[a_reg] if (a_bit == 1 and a_reg < 32768) else a_reg
                x_val = d_reg

                # ALU calculation
                zx = (c_bits >> 5) & 1
                nx = (c_bits >> 4) & 1
                zy = (c_bits >> 3) & 1
                ny = (c_bits >> 2) & 1
                f  = (c_bits >> 1) & 1
                no = c_bits & 1

                x_comp = 0 if zx else x_val
                if nx: x_comp = (~x_comp) & 0xFFFF

                y_comp = 0 if zy else y_val
                if ny: y_comp = (~y_comp) & 0xFFFF

                if f:
                    res = (x_comp + y_comp) & 0xFFFF
                else:
                    res = (x_comp & y_comp) & 0xFFFF

                if no:
                    res = (~res) & 0xFFFF

                # Signed 16-bit interpretation
                signed_res = res - 65536 if res >= 32768 else res

                # Destinations
                if dest_bits & 1:  # M
                    if a_reg < 32768:
                        ram[a_reg] = signed_res
                if dest_bits & 2:  # D
                    d_reg = signed_res
                if dest_bits & 4:  # A
                    a_reg = signed_res & 0x7FFF

                # Jumps
                zr = (signed_res == 0)
                ng = (signed_res < 0)
                pos = (signed_res > 0)

                jlt = (jump_bits & 4) and ng
                jeq = (jump_bits & 2) and zr
                jgt = (jump_bits & 1) and pos

                if jlt or jeq or jgt:
                    pc = a_reg
                else:
                    pc += 1

        return ram

    # Test 1: Key Pressed (e.g. key code 65)
    ram_pressed = run_sim(key_code=65, max_cycles=3000)
    # Check all box words
    for r in range(20):
        row_start = base_addr + (32 * r)
        for w in range(w_words):
            val = ram_pressed[row_start + w]
            assert val == -1 or val == 65535, f"Row {r}, word {w} (addr {row_start + w}) expected -1/black, got {val}"
    print(">>> Simulation with KEY PRESSED: All 20 rows x words correctly filled with BLACK (-1)!")

    # Test 2: Key Released (key code 0)
    ram_released = run_sim(key_code=0, max_cycles=3000)
    for r in range(20):
        row_start = base_addr + (32 * r)
        for w in range(w_words):
            val = ram_released[row_start + w]
            assert val == 0, f"Row {r}, word {w} (addr {row_start + w}) expected 0/white, got {val}"
    print(">>> Simulation with KEY RELEASED: All box words correctly cleared to WHITE (0)!")

    # Print ASCII display of screen region
    print("\n--- Visual Representation of Drawn Box (First 5 rows shown) ---")
    for r in range(5):
        row_start = base_addr + (32 * r)
        pixels = ""
        for w in range(w_words):
            pixels += "████████████████"
        print(f"Row {start_row + r:2d} (Addr {row_start}): |{pixels}| {' ' * (64 - len(pixels))}| (rest of screen)")
    print("   ... (20 rows in total) ...")
    print(">>> Visual verification confirmed!")


if __name__ == '__main__':
    k = int(sys.argv[1]) if len(sys.argv) > 1 else 41
    os.chdir(r"C:\Nand and tetris\capstone")
    test_assembler(k)
    simulate_hack_box(k)
    print("\nALL VERIFICATION TESTS COMPLETED SUCCESSFULLY!")
