# CAPSTONE PROJECT REPORT
## MAKE THE COMPUTER DRAW A BOX

**Course:** Nand to Tetris – I  
**Subject Code:** ETCNTC301 / ETCCNT301  
**Program:** B.Tech Computer Science & Engineering (AI & ML)  
**School:** School of Engineering & Technology, K.R. Mangalam University  
**Mode:** Individual Work  

---

### Student Information & Personal Number ($K$)

- **Student Name:** Pawan Kumar Singh
- **University Roll Number:** 2501730252
- **Course / Branch:** B.Tech CSE (AI & ML) - Semester III
- **Subject Name:** Nand to Tetris – I
- **Subject Code:** ETCNTC301 (ETCCNT301)
- **Personal Number ($K$):** Last two digits of Roll Number = **52**

#### Parameter Calculations for $K = 52$:
- **Assembler Feature Index:** $K \pmod 3 = 52 \pmod 3 = 1$
  - **Assigned Additional Feature:** For an incorrect instruction, print a clear error message with the line number (e.g., `Line 7: invalid instruction: ...`) instead of crashing.
- **Box Width Calculation:**
  - $K \pmod 4 = 52 \pmod 4 = 0$
  - **Words per Row:** $(K \pmod 4) + 1 = 0 + 1 = 1\text{ 16-bit word per row}$
  - **Box Width in Pixels:** $16 \times 1 = 16\text{ pixels}$
- **Box Starting Row:** $\text{Row } K = \text{Row } 52$
- **Box Height:** $20\text{ screen rows}$ (Consecutive rows 52 through 71)
- **Screen Base Memory Address:**
  $$\text{Address} = \text{SCREEN} + 32 \times K = 16384 + (32 \times 52) = 16384 + 1664 = \mathbf{18048} \quad (0\text{x}4680)$$

---

### 1. Part A – Hack Computer HDL Implementation

The Hack Computer was constructed using three integrated chips:

#### A. Central Processing Unit (`CPU.hdl`)
- **Instruction Decoding:**
  - Bit 15 determines instruction type: `0` indicates an A-instruction (loads 15-bit address/constant into the A register), while `1` indicates a C-instruction (`111 a c1 c2 c3 c4 c5 c6 d1 d2 d3 j1 j2 j3`).
  - Mux16 selects between the raw instruction bits (for A-instructions) and the ALU output (`outALU`, for C-instructions) as input to the A register.
  - A register loading condition: `loadA = isA | (isC & instruction[5])`.
  - D register loading condition: `loadD = isC & instruction[4]`.
  - Mux16 selects between the A register and incoming memory value `inM` based on the $a$-bit (`instruction[12]`).
- **ALU Operation:**
  - The Hack ALU computes arithmetic and logic functions dictated by control bits $c_1$ through $c_6$ (`instruction[11..6]`).
  - Produces computation result `outM`, zero flag `zr` ($out == 0$), and negative flag `ng` ($out < 0$).
- **Program Counter (PC) & Conditional Jump Logic:**
  - Determines positive status: `pos = !(zr | ng)`.
  - Evaluates jump conditions:
    - $j_1 \land ng$ (`jlt`: jump if out < 0)
    - $j_2 \land zr$ (`jeq`: jump if out == 0)
    - $j_3 \land pos$ (`jgt`: jump if out > 0)
  - When any valid jump condition is satisfied during a C-instruction, `loadPC = 1` loads the address from the A register into PC; otherwise `inc = true` fetches the next sequential instruction.

#### B. Memory Architecture (`Memory.hdl`)
- Memory mapping:
  - Addresses `0` to `16383` ($0\text{x}0000 - 0\text{x}3\text{FFF}$): 16K Data RAM (`RAM16K`).
  - Addresses `16384` to `24575` ($0\text{x}4000 - 0\text{x}5\text{FFF}$): 8K Screen memory map (`Screen`).
  - Address `24576` ($0\text{x}6000$): Keyboard memory-mapped register (`Keyboard`).
- Address routing is handled via `DMux4Way` and `Mux4Way16` based on address bits `address[13..14]`.

#### C. Top-Level Integration (`Computer.hdl`)
- Integrates `ROM32K`, `CPU`, and `Memory`:
  - `ROM32K(address=pc, out=instruction)`
  - `CPU(inM=inM, instruction=instruction, reset=reset, outM=outM, writeM=writeM, addressM=addressM, pc=pc)`
  - `Memory(in=outM, load=writeM, address=addressM, out=inM)`
- Reset mechanism restarts execution from ROM address 0 when `reset == 1`.

---

### 2. Part B – Two-Pass Python Assembler (`assembler.py`)

The assembler converts Hack assembly code (`.asm`) into binary machine language (`.hack`):

#### A. Pass 1: Label Processing & Symbol Table Creation
1. Reads all assembly lines, strips whitespace and comments (`//...`).
2. Discards blank lines.
3. Maintains a running count of ROM instruction memory addresses (`rom_address`).
4. On encountering a label declaration `(LABEL)`, records `symbol_table[label] = rom_address`.
5. Labels do not increment the ROM address counter.

#### B. Pass 2: Binary Code Generation & Variable Allocation
1. Translates A-instructions `@value`:
   - If `@number`: formats the constant directly into a 16-bit binary string (`0` + 15-bit address).
   - If `@symbol`: checks the symbol table. If not found, allocates the next available RAM address starting from RAM address 16 ($16, 17, 18, \dots$) and records it in `symbol_table`.
2. Translates C-instructions `dest = comp ; jump`:
   - Encodes as `111` + `comp (7 bits)` + `dest (3 bits)` + `jump (3 bits)`.

#### C. Personal Extra Feature for $K = 52$ ($K \pmod 3 = 1$)
- Implemented syntax error diagnostics. When an invalid mnemonic or unrecognized instruction format is parsed, the assembler identifies the exact line number in the source file and outputs a clear diagnostic:
  ```text
  Line 3: invalid instruction (Invalid comp expression 'INVALID_INSTRUCTION' in 'INVALID_INSTRUCTION')
  ```
  The assembler reports all syntax errors gracefully without crashing unhandled.
- Furthermore, symbol tables are cleanly exported to `symbols.txt` for complete debugging visibility.

---

### 3. Part C – Box Assembly Program (`Box.asm`)

#### A. Mathematical Dimensions & Memory Layout ($K = 52$)
- Screen Resolution: $512 \times 256$ pixels.
- Row Pitch: Each screen row consists of 32 16-bit words ($32 \times 16 = 512$ pixels).
- Base Address Formula: $\text{SCREEN} + 32 \times K = 16384 + (32 \times 52) = 18048$.
- Width: $16 \times ((52 \pmod 4) + 1) = 16\text{ pixels}$ (1 word per row).
- Height: 20 rows (Rows 52 through 71).
- Memory Addresses Written:
  - Row 52: RAM[18048]
  - Row 53: RAM[18080]
  - Row 54: RAM[18112]
  - $\dots$
  - Row 71: RAM[18656]

#### B. Continuous Keyboard Interaction Flow
1. **Poll Keyboard:** Reads RAM[24576] (`@KBD`).
2. **State Selection:**
   - Key pressed (`RAM[KBD] != 0`): Sets `color = -1` ($0\text{xFFFF}$, black).
   - Key released (`RAM[KBD] == 0`): Sets `color = 0` ($0\text{x0000}$, white/cleared).
3. **Optimized Screen Write Loop:**
   - Sets `row_addr = 18048` and `row_count = 20`.
   - In each row iteration, writes `color` into `RAM[row_addr]`.
   - Increments `row_addr` by 32 using `M=D+M`.
   - Decrements `row_count` until 0.
4. **Infinite Loop:** Jumps back to `MAIN_LOOP` to sample the keyboard register again.

---

### 4. Official Test Results & Verification

All tests were verified through official test scripts and cycle-accurate simulation:
1. **HDL Chips:** Passed official test files `CPU.tst`, `Memory.tst`, and `ComputerAdd.tst`.
2. **Python Assembler:**
   - Assembled `Add.asm` into `Add.hack`; verified 100% bit-exact match against official Hack test files.
   - Verified line-numbered syntax error reporting for $K \pmod 3 = 1$.
   - Verified duplicate label warning for $K \pmod 3 = 2$.
   - Verified export of labels and user variables to `symbols.txt`.
3. **Hack CPU Simulation of Box.asm ($K = 52$):**
   - **Key Pressed:** All 20 words (from RAM[18048] to RAM[18656]) verified as $-1$ (black).
   - **Key Released:** All 20 words verified as $0$ (white).
   - Real-time ASCII rasterization confirmed the $16\text{ px} \times 20\text{ row}$ box rendered from the left edge of row 52.

---

### 5. Programming Mistake Encountered & Solution

- **Encountered Mistake:** During the initial build of `Box.asm`, calculating the next row address via `@32; D=A; @row_addr; M=M+D` resulted in an assembler error: `Invalid comp expression 'M+D'`.
- **Root Cause:** In the Hack ALU hardware architecture, addition is defined as $D+A$ and $D+M$. The Hack Assembly standard requires $D$ as the left-hand operand when adding to memory.
- **Correction:**
  1. Updated `Box.asm` to use `M=D+M`.
  2. Enhanced `assembler.py` to also accept commutative variants (`M+D`, `M&D`, `M|D`) for enhanced parser robustness.

---

### 6. Viva Preparation Questions & Key Answers

1. **Explain the CPU.hdl decoding logic:**
   - Bit 15 determines A/C instruction. In C-instructions, bits 11..6 control the 6 ALU flags (`zx, nx, zy, ny, f, no`), bit 12 selects A or M, bits 5..3 select destinations (A, D, M), and bits 2..0 govern conditional branching based on ALU flags (`zr`, `ng`).
2. **How Hack Screen Memory is organized:**
   - Screen memory starts at address 16384 (`0x4000`) and occupies 8192 words (256 rows $\times$ 32 words/row). Address for row $r$, word $c$ is $\text{SCREEN} + 32 \times r + c$.
3. **How to modify the program on the spot during Viva:**
   - *Move box down by 10 rows:* Change starting address from `@18048` to `@18368` (since $18048 + 32 \times 10 = 18368$).
   - *Change box height to 30 rows:* Change `@20` to `@30` at `row_count` initialization.
   - *Change box width to 32 pixels:* Add an extra write `A=A+1; M=D` inside the row loop to color word 1 in each row.
