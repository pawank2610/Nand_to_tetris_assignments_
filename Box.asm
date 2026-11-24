// ==================================================================
// Capstone Project: Box.asm
// Course: Nand to Tetris - I (ETCNTC301)
// School of Engineering & Technology, K.R. Mangalam University
//
// Personal Number K       : 52
// Starting Row            : 52
// Box Height              : 20 rows
// Box Width               : 16 pixels (1 16-bit word(s) per row)
// Screen Base Address     : SCREEN + 32 * 52 = 16384 + 1664 = 18048
// ==================================================================

(MAIN_LOOP)
    // Step 1: Read Keyboard memory-mapped register (address 24576)
    @KBD
    D=M
    @KEY_PRESSED
    D;JNE               // If RAM[KBD] != 0, key is pressed -> jump to KEY_PRESSED

    // Step 2a: No key pressed -> set color to 0 (white / clear box)
    @color
    M=0
    @START_DRAW
    0;JMP

(KEY_PRESSED)
    // Step 2b: Key is pressed -> set color to -1 (black: all 16 bits = 1)
    @color
    M=-1

(START_DRAW)
    // Step 3: Initialize row address to starting row address: 18048
    @18048
    D=A
    @row_addr
    M=D

    // Step 4: Initialize row counter to 20 rows
    @20
    D=A
    @row_count
    M=D

(ROW_LOOP)
    // Check if all 20 rows have been drawn
    @row_count
    D=M
    @MAIN_LOOP
    D;JEQ               // If row_count == 0, finished drawing -> loop back to KBD check

    // Step 5: Draw 1 word(s) across the current row starting from left edge
    @color
    D=M
    @row_addr
    A=M
    M=D                 // Word 0

    // Step 6: Advance row_addr to next screen row (next row starts at row_addr + 32)
    @32
    D=A
    @row_addr
    M=D+M

    // Step 7: Decrement row_count
    @row_count
    M=M-1

    // Loop back to draw next row
    @ROW_LOOP
    0;JMP
