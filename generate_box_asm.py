"""
Box.asm Generator for Nand to Tetris Capstone Project
Calculates dimensions and base addresses from Personal Number K,
and outputs fully documented Box.asm.
"""

import sys
import os

def generate_box_asm(k):
    start_row = k
    height = 20
    w_words = (k % 4) + 1
    width_px = 16 * w_words
    base_addr = 16384 + (32 * k)

    asm_lines = [
        f"// ==================================================================",
        f"// Capstone Project: Box.asm",
        f"// Course: Nand to Tetris - I (ETCNTC301)",
        f"// School of Engineering & Technology, K.R. Mangalam University",
        f"//",
        f"// Personal Number K       : {k}",
        f"// Starting Row            : {start_row}",
        f"// Box Height              : {height} rows",
        f"// Box Width               : {width_px} pixels ({w_words} 16-bit word(s) per row)",
        f"// Screen Base Address     : SCREEN + 32 * {k} = 16384 + {32 * k} = {base_addr}",
        f"// ==================================================================",
        f"",
        f"(MAIN_LOOP)",
        f"    // Step 1: Read Keyboard memory-mapped register (address 24576)",
        f"    @KBD",
        f"    D=M",
        f"    @KEY_PRESSED",
        f"    D;JNE               // If RAM[KBD] != 0, key is pressed -> jump to KEY_PRESSED",
        f"",
        f"    // Step 2a: No key pressed -> set color to 0 (white / clear box)",
        f"    @color",
        f"    M=0",
        f"    @START_DRAW",
        f"    0;JMP",
        f"",
        f"(KEY_PRESSED)",
        f"    // Step 2b: Key is pressed -> set color to -1 (black: all 16 bits = 1)",
        f"    @color",
        f"    M=-1",
        f"",
        f"(START_DRAW)",
        f"    // Step 3: Initialize row address to starting row address: {base_addr}",
        f"    @{base_addr}",
        f"    D=A",
        f"    @row_addr",
        f"    M=D",
        f"",
        f"    // Step 4: Initialize row counter to {height} rows",
        f"    @{height}",
        f"    D=A",
        f"    @row_count",
        f"    M=D",
        f"",
        f"(ROW_LOOP)",
        f"    // Check if all {height} rows have been drawn",
        f"    @row_count",
        f"    D=M",
        f"    @MAIN_LOOP",
        f"    D;JEQ               // If row_count == 0, finished drawing -> loop back to KBD check",
        f"",
        f"    // Step 5: Draw {w_words} word(s) across the current row starting from left edge",
        f"    @color",
        f"    D=M",
        f"    @row_addr",
        f"    A=M",
        f"    M=D                 // Word 0",
    ]

    for w_idx in range(1, w_words):
        asm_lines.extend([
            f"    A=A+1",
            f"    M=D                 // Word {w_idx}",
        ])

    asm_lines.extend([
        f"",
        f"    // Step 6: Advance row_addr to next screen row (next row starts at row_addr + 32)",
        f"    @32",
        f"    D=A",
        f"    @row_addr",
        f"    M=D+M",
        f"",
        f"    // Step 7: Decrement row_count",
        f"    @row_count",
        f"    M=M-1",
        f"",
        f"    // Loop back to draw next row",
        f"    @ROW_LOOP",
        f"    0;JMP",
        f""
    ])

    return "\n".join(asm_lines)

if __name__ == '__main__':
    k_arg = int(sys.argv[1]) if len(sys.argv) > 1 else 41
    content = generate_box_asm(k_arg)
    out_file = sys.argv[2] if len(sys.argv) > 2 else "Box.asm"
    with open(out_file, "w") as f:
        f.write(content)
    print(f"Generated {out_file} for K = {k_arg}")
