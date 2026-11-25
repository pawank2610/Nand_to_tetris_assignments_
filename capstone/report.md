# Capstone Project Report
## Make the Computer Draw a Box

**Student Name:** Pawan Kr. Singh  
**Roll Number:** 2501730252  
**Course:** Nand to Tetris – I (ETCNTC301)  
**School:** School of Engineering & Technology  
**University:** K.R. Mangalam University  
**Personal Parameter $K$:** **52** ($52 \bmod 3 = 1$, $52 \bmod 4 = 0$)  

---

## 1. Personal Project Calculations ($K = 52$)

Derived from the last two digits of university roll number **2501730252**:
- **Personal Number $K$:** $52$
- **Starting Screen Row:** Equal to $K = \mathbf{52}$
- **Box Height:** $20$ consecutive screen rows (Row 52 to Row 71)
- **Box Width:** $\text{Width} = 16 \times ((K \bmod 4) + 1) = 16 \times ((52 \bmod 4) + 1) = 16 \times (0 + 1) = \mathbf{16\text{ pixels}}$
- **Words per Row:** $16 / 16 = \mathbf{1\text{ word per row}}$
- **Starting Screen Address:** $\text{SCREEN} + (32 \times 52) = 16384 + 1664 = \mathbf{18048}$
- **Ending Screen Address:** $16384 + (32 \times 71) = 16384 + 2272 = \mathbf{18656}$
- **Total Screen Words Modified:** $20\text{ rows} \times 1\text{ word} = \mathbf{20\text{ words}}$ ($320\text{ pixels}$)
- **Additional Assembler Feature ($K \bmod 3 = 52 \bmod 3 = 1$):** Invalid instruction error handling with exact source line numbers (`Line <N>: invalid instruction`).

---

## 2. Part A: Hack Computer Architecture (HDL)
Integrated and verified the complete 16-bit Hack computer hardware:
- **`CPU.hdl`:** Instruction decoding, ALU operations, A/D register routing, and conditional jump control.
- **`Memory.hdl`:** Address space decoding partitioning RAM16K (`0..16383`), Screen memory (`16384..24575`), and Keyboard register (`24576`).
- **`Computer.hdl`:** Integrates CPU, Memory, and ROM32K.
- **Test Verification:** Passed official `CPU.tst`, `Memory-auto.tst`, and `ComputerRect.tst` with zero mismatches.

---

## 3. Part B: Two-Pass Python Hack Assembler (`assembler.py`)
- **Pass 1:** Scans source code, strips comments and whitespace, tracks ROM addresses, and populates the symbol table. Detects malformed/duplicate labels and raises line-numbered exceptions.
- **Pass 2:** Synthesizes 16-bit binary machine code, assigns RAM variables starting at address 16, and validates instruction grammar.
- **Benchmarking:** Tested against `Add.asm`, `Max.asm`, `Rect.asm`, and `Pong.asm` (27,483 instructions), matching reference `.hack` files 100% byte-for-byte.

---

## 4. Part C: Box Drawing Program (`Box.asm`)
Continuously polls keyboard register `RAM[24576]`:
1. If any key is pressed ($D \ne 0$), sets color to black ($-1$).
2. If key is released ($D == 0$), sets color to white ($0$).
3. Loops through 20 rows, writing the color to 1 word per row starting from address **18048** down to **18656**.
4. Prominently loads student personal number **52** into register D (`@52; D=A`).

---

## 5. One Programming Mistake Encountered and Corrected
**The Issue:** Attempting to advance the screen pointer using `M=M+D` threw an invalid computation syntax error because Hack ALU does not support `M+D` as a single instruction (it only supports `D+M`).  
**The Fix:** Structured the pointer arithmetic cleanly as `D=D+M; @row_ptr; M=D`, ensuring 100% compliant Hack assembly syntax.
