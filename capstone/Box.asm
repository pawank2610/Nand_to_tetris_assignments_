// ==================================================================
// Box.asm - Make the Computer Draw a Box
// Student: Pawan Kr. Singh
// Roll Number: 2501730252
// Course: Nand to Tetris - I (ETCNTC301)
// University: K.R. Mangalam University
//
// Personal Number K = 52
// Calculations for K = 52:
// - Starting row: 52 (Row 52 of 256)
// - Ending row: 52 + 20 - 1 = 71 (Height = 20 rows)
// - Starting column: 0 (leftmost edge)
// - Width formula: 16 * ((K mod 4) + 1)
//   52 mod 4 = 0
//   Width = 16 * (0 + 1) = 16 pixels (exactly 1 word per row)
// - First screen address: SCREEN + (32 * 52) = 16384 + 1664 = 18048
// - Last screen address:  16384 + (32 * 71) = 16384 + 2272 = 18656
// - Total screen words modified: 20 * 1 = 20 words (320 pixels)
//
// Register D output: Displays 52 (student personal number K)
// ==================================================================

(MAIN_LOOP)
    // Put Personal Number K = 52 into D register
    @52
    D=A

    // Step 1: Read keyboard register KBD (address 24576)
    @KBD
    D=M

    // If key is pressed (KBD != 0), jump to KEY_PRESSED to set black
    @KEY_PRESSED
    D;JNE

    // Otherwise, key released (KBD == 0): set color to white (0)
    @color
    M=0
    @DRAW_BOX
    0;JMP

(KEY_PRESSED)
    // Key is pressed: set color to black (-1 = 1111111111111111)
    @color
    M=-1

(DRAW_BOX)
    // Initialize screen pointer to first address of row 52
    // 16384 + (32 * 52) = 18048
    @18048
    D=A
    @row_ptr
    M=D

    // Initialize row counter to 20 rows
    @20
    D=A
    @row_count
    M=D

(ROW_LOOP)
    // Check if all 20 rows have been drawn
    @row_count
    D=M
    @FINISH_FRAME
    D;JEQ           // When finished 20 rows, jump to finish

    // Load color into D register
    @color
    D=M

    // Draw 1 word per row (16 pixels wide for K=52)
    @row_ptr
    A=M
    M=D

    // Advance pointer to the start of the next screen row
    // Since only 1 word was drawn, advance by 32 words to reach next row
    @32
    D=A
    @row_ptr
    D=D+M
    @row_ptr
    M=D

    // Decrement row counter
    @row_count
    M=M-1

    @ROW_LOOP
    0;JMP

(FINISH_FRAME)
    // Ensure register D displays student personal number 52
    @52
    D=A

    // Loop back to poll keyboard again
    @MAIN_LOOP
    0;JMP
