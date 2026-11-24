# Nand to Tetris - I (ETCNTC301)
## Capstone Project: Make the Computer Draw a Box
**School of Engineering & Technology, K.R. Mangalam University**

---

### Project Structure in `capstone/`

- **Part A: Hack Computer HDL Implementation**
  - `CPU.hdl` : Complete Hack Central Processing Unit implementation.
  - `Memory.hdl` : Complete memory chip (RAM16K, Screen memory map, Keyboard register).
  - `Computer.hdl` : Top-level Hack Computer wiring CPU, Memory, and ROM32K.
  - Official test scripts & comparison outputs: `CPU.tst`, `CPU.cmp`, `Memory.tst`, `Memory.cmp`, `ComputerAdd.tst`, `ComputerAdd.cmp`.

- **Part B: Two-Pass Python Assembler**
  - `assembler.py` : Two-pass assembler converting `.asm` to `.hack`.
  - Implements all extra features based on $K \pmod 3$:
    - $K \pmod 3 = 0$: Exports full symbol table to `symbols.txt`.
    - $K \pmod 3 = 1$: Enhanced line-numbered error diagnostics (e.g. `Line 7: invalid instruction`).
    - $K \pmod 3 = 2$: Duplicate label detection warning.
  - Generates `symbols.txt` automatically.

- **Part C: Box Drawing Assembly Program**
  - `Box.asm` : Hack Assembly program that monitors `KBD` and draws/erases the rectangular box.
  - `Box.hack` : Assembled 16-bit binary machine code ready to run on CPU Emulator.
  - `generate_box_asm.py` : Parametric generator for any Roll Number $K$.
  - `verify_capstone.py` : Verification and CPU execution test suite.

---

### Quick Commands

1. **Generate Box.asm for your personal number K (e.g., K = 41):**
   ```bash
   python generate_box_asm.py 41
   ```

2. **Assemble Box.asm to Box.hack using your Python Assembler:**
   ```bash
   python assembler.py Box.asm 41
   ```

3. **Run Full Verification Suite:**
   ```bash
   python verify_capstone.py 41
   ```
