# Individual Viva Voce Guide • Pawan Kr. Singh (Roll: 2501730252, K = 52)
## Nand to Tetris Capstone Project — "Make the Computer Draw a Box"

### 1. Elevator Pitch (Start Your Viva With This)
> *"Good morning, Examiner. My capstone project implements the entire vertical computer system for student personal number **K = 52**, derived from my roll number **2501730252**.
> In **Part A**, I integrated CPU.hdl, Memory.hdl, and Computer.hdl, all verified on the official Hardware Simulator.
> In **Part B**, I built a two-pass assembler in Python (`assembler.py`) with line-number error reporting for \(52 \bmod 3 = 1\), matching benchmark files byte-for-byte.
> In **Part C**, I authored `Box.asm` which continuously polls the keyboard at address 24576. When any key is pressed, it draws a solid black rectangle of width 16 pixels across 20 rows starting at row 52 from address 18048 to 18656 (modifying 20 words), and clears it on release."*

### 2. Key Mathematical Derivations ($K = 52$)
- **Starting Row:** Equal to $K = \mathbf{52}$.
- **Box Height:** $20$ consecutive rows (Rows 52 to 71).
- **Width Formula:** \(16 \times ((K \bmod 4) + 1) = 16 \times ((52 \bmod 4) + 1) = 16 \times (0 + 1) = \mathbf{16\text{ pixels}}\) (1 word per row).
- **Starting Screen Address:** \(16384 + (32 \times 52) = 16384 + 1664 = \mathbf{18048}\).
- **Ending Screen Address:** \(16384 + (32 \times 71) = 16384 + 2272 = \mathbf{18656}\).
- **Total Screen Words Modified:** \(20 \times 1 = \mathbf{20\text{ words}}\) (320 pixels).

### 3. Live Viva Modification: "Move the box down by 1 row"
1. Open `Box.asm`.
2. Change starting address from row 52 (`@18048`) to row 53:
   \[16384 + (32 \times 53) = 16384 + 1696 = \mathbf{18080}\]
3. Reassemble with `python3 assembler.py Box.asm Box.hack` and run in the CPU Emulator!
