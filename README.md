# Nand to Tetris - I (ETCNTC301)
## Capstone Project & Course Assignments
**School of Engineering & Technology, K.R. Mangalam University**

- **Student Name:** Pawan Kr. Singh
- **Roll Number:** 2501730252
- **Personal Number ($K$):** Last two digits of Roll Number = **52**
- **Live Interactive Lab (GitHub Pages):** [https://pawank2610.github.io/Nand_to_tetris_assignments_/](https://pawank2610.github.io/Nand_to_tetris_assignments_/)

---

## 🌟 Interactive Capstone Lab

Explore the complete interactive simulation and hardware architecture directly in your browser:
👉 **[Open Live Web Dashboard & Simulator](https://pawank2610.github.io/Nand_to_tetris_assignments_/)**

Features included in the web app (`index.html`):
- **Live Screen Display Simulator:** Real-time 512×256 Hack screen showing the interactive 16×20 pixel Box at Row 52 (Screen address 18048..18656) with interactive Keyboard trigger.
- **CPU & Memory Architecture Diagram:** Visual datapath showing ALU, A-register, D-register, PC, Screen map, and RAM16K.
- **Two-Pass Python Assembler Inspector:** Live assembler emulator with symbol table generation (`symbols.txt`) and line-numbered syntax diagnostic validation.
- **Full Capstone Report & Viva Guide:** Built-in technical documentation and oral examination preparation notes.

---

## 📁 Repository Structure

```
.
├── index.html                   # Interactive Capstone Lab & Visualizer (GitHub Pages entry)
├── dashboard.html               # Lab Dashboard
├── report.md                    # Comprehensive Capstone Project Report
├── VIVA_GUIDE.md                # Viva voce preparation questions & answers
│
├── HDL/                         # Hardware Description Language implementations & tests
│   ├── CPU.hdl                  # 16-bit Hack CPU implementation
│   ├── CPU.tst / CPU.cmp        # Official Hardware Simulator test scripts & comparison
│   ├── Memory.hdl               # Hack Memory (RAM16K + Screen + Keyboard)
│   ├── Memory.tst / Memory.cmp  # Memory test script & comparison
│   ├── Computer.hdl             # Complete Hack Computer wiring CPU, Memory & ROM
│   └── ComputerAdd.tst / .cmp   # Full computer execution test suite
│
├── assembler.py                 # Custom Two-Pass Hack Assembler (Python 3)
├── symbols.txt                  # Exported symbol table from Pass 1
├── assembler/                   # Official benchmarks & reference outputs
│   ├── Add.asm / Add.ref.hack
│   ├── Max.asm / Max.ref.hack
│   ├── Rect.asm / Rect.ref.hack
│   └── Pong.asm / Pong.ref.hack (27,483 instructions benchmark)
│
├── Box.asm                      # Parametric Box drawing Hack assembly program (K=52)
├── Box.hack                     # Assembled 16-bit binary machine code
│
├── tests/                       # Automated test suite
│   └── test_assembler.py        # 16 comprehensive unit tests (all passing)
│
├── screenshots/                 # Hardware & software verification screenshots
│   ├── CPU_test.png
│   ├── Memory_test.png
│   ├── Computer_test.png
│   ├── assembler_test.png
│   ├── box_visible.png
│   └── box_cleared.png
│
├── Pawan_Kumar_Singh_2501730252_Capstone_Report.pdf  # Final compiled PDF report
├── Assignment_1_Nand_To_Tetris.docx.pdf              # Assignment 1 submission
├── Assignment_2_nand_to_tetris.pdf                   # Assignment 2 submission
└── Q2..Q5 docx files                                # Lab assignment documentation
```

---

## 🧮 Capstone Parameters for $K = 52$

- **Personal Number $K$:** $52$ (Roll: 2501730252)
- **Assembler Feature ($K \bmod 3 = 1$):** Clear error reporting with exact line numbers (`Line <N>: invalid instruction`) instead of crashing.
- **Starting Screen Row:** Equal to $K = \mathbf{52}$
- **Box Height:** $20$ consecutive screen rows (Row 52 to Row 71)
- **Words per Row:** $(K \bmod 4) + 1 = (52 \bmod 4) + 1 = \mathbf{1\text{ word (16 pixels)}}$
- **Screen Memory Addresses:**
  - Start: $\text{SCREEN} + (32 \times 52) = 16384 + 1664 = \mathbf{18048}$
  - End: $16384 + (32 \times 71) = 16384 + 2272 = \mathbf{18656}$
- **Total Screen Words:** $20\text{ words}$ ($320\text{ pixels}$)

---

## 🚀 Quick Execution

### 1. Run the Python Assembler
```bash
python3 assembler.py Box.asm Box.hack
```

### 2. Run the Unit Test Suite
```bash
python3 tests/test_assembler.py
```

### 3. Launch the Web Visualizer Locally
```bash
# Open directly in your browser:
open index.html
```

---

## 📄 License
Academic coursework for Nand to Tetris – I (ETCNTC301), School of Engineering & Technology, K.R. Mangalam University.
