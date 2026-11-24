"""
Generates the complete, professional All-in-One Capstone Project PDF
for Pawan Kumar Singh (Roll No: 2501730252, K = 52).
"""

import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Preformatted, HRFlowable
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_header_footer(num_pages)
            super().showPage()
        super().save()

    def draw_header_footer(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#555555"))
        
        # Omit header and footer on cover page (page 1)
        if self._pageNumber > 1:
            # Header
            self.drawString(54, 750, "Nand to Tetris – I (ETCNTC301) | Capstone Project: Make the Computer Draw a Box")
            self.drawRightString(612 - 54, 750, "Pawan Kumar Singh (2501730252)")
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.5)
            self.line(54, 744, 612 - 54, 744)
            
            # Footer
            self.line(54, 45, 612 - 54, 45)
            self.drawString(54, 32, "School of Engineering & Technology, K.R. Mangalam University")
            page_text = f"Page {self._pageNumber} of {page_count}"
            self.drawRightString(612 - 54, 32, page_text)
            
        self.restoreState()


def build_pdf():
    pdf_filename = r"C:\Nand and tetris\capstone\Pawan_Kumar_Singh_2501730252_Capstone_Report.pdf"
    doc = SimpleDocTemplate(
        pdf_filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Custom typography styles
    title_style = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=30,
        alignment=1,
        textColor=colors.HexColor("#0B2545")
    )

    subtitle_style = ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=17,
        alignment=1,
        textColor=colors.HexColor("#1E3A8A")
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        spaceBefore=14,
        spaceAfter=6,
        textColor=colors.HexColor("#0B2545"),
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        spaceBefore=9,
        spaceAfter=4,
        textColor=colors.HexColor("#1E3A8A"),
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        spaceAfter=5,
        textColor=colors.HexColor("#1E293B")
    )

    code_style = ParagraphStyle(
        'Code_Custom',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=7.2,
        leading=9.2,
        textColor=colors.HexColor("#0F172A"),
        backColor=colors.HexColor("#F1F5F9"),
        borderPadding=5,
        spaceBefore=3,
        spaceAfter=5
    )

    story = []

    # ==========================================
    # COVER PAGE
    # ==========================================
    story.append(Spacer(1, 35))
    story.append(Paragraph("K.R. MANGALAM UNIVERSITY", subtitle_style))
    story.append(Paragraph("SCHOOL OF ENGINEERING & TECHNOLOGY", ParagraphStyle('SubSub', parent=subtitle_style, fontName='Helvetica-Bold', fontSize=10, textColor=colors.HexColor("#475569"))))
    story.append(Spacer(1, 10))
    story.append(HRFlowable(width="85%", thickness=2.5, color=colors.HexColor("#0B2545"), spaceAfter=20, spaceBefore=10))
    story.append(Spacer(1, 10))

    story.append(Paragraph("CAPSTONE PROJECT REPORT", ParagraphStyle('LabelProj', parent=subtitle_style, fontName='Helvetica-Bold', fontSize=13, textColor=colors.HexColor("#2563EB"))))
    story.append(Spacer(1, 8))
    story.append(Paragraph("MAKE THE COMPUTER DRAW A BOX", title_style))
    story.append(Spacer(1, 8))
    story.append(Paragraph("Construction of Hack Computer (HDL), Two-Pass Python Assembler, and Screen Driver Assembly Program", subtitle_style))
    story.append(Spacer(1, 25))

    # Student Info Table Box
    info_data = [
        [Paragraph("<b>Student Name</b>", body_style), Paragraph("<b>Pawan Kumar Singh</b>", body_style)],
        [Paragraph("<b>University Roll Number</b>", body_style), Paragraph("<b>2501730252</b>", body_style)],
        [Paragraph("<b>Academic Degree / Branch</b>", body_style), Paragraph("<b>B.Tech Computer Science & Engineering (AI & ML)</b>", body_style)],
        [Paragraph("<b>Current Semester</b>", body_style), Paragraph("Semester III", body_style)],
        [Paragraph("<b>Course Name</b>", body_style), Paragraph("<b>Nand to Tetris – I</b>", body_style)],
        [Paragraph("<b>Subject Code</b>", body_style), Paragraph("<b>ETCNTC301 / ETCCNT301</b>", body_style)],
        [Paragraph("<b>Personal Number (K)</b>", body_style), Paragraph("<b>52</b> (Last 2 digits of Roll Number 2501730252)", body_style)],
        [Paragraph("<b>Submission Mode</b>", body_style), Paragraph("Individual Capstone Project", body_style)],
    ]
    t_info = Table(info_data, colWidths=[170, 310])
    t_info.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F8FAFC")),
        ('BOX', (0,0), (-1,-1), 1.5, colors.HexColor("#0B2545")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(t_info)

    story.append(Spacer(1, 35))
    story.append(Paragraph("Department of Computer Science & Engineering<br/>Academic Session 2026–2027", ParagraphStyle('FooterCover', parent=subtitle_style, fontSize=9.5, textColor=colors.HexColor("#64748B"))))

    story.append(PageBreak())

    # ==========================================
    # SECTION 1: EXECUTIVE SUMMARY & K DERIVATION
    # ==========================================
    story.append(Paragraph("1. Executive Summary & Personal Number (K) Derivation", h1_style))
    story.append(Paragraph(
        "This capstone project realizes the full vertical stack of a general-purpose computing system "
        "as specified in the Nand to Tetris curriculum. The project spans three hierarchical tiers: "
        "<br/>1. <b>Hardware Level:</b> Implementing and validating a complete 16-bit Hack CPU, Memory Map, and Computer in HDL; "
        "<br/>2. <b>Systems Software Level:</b> Engineering a complete two-pass assembler in Python with label resolution, symbol allocation, and line-numbered syntax diagnostics; and "
        "<br/>3. <b>Application Level:</b> Authoring an interactive Hack assembly program (<code>Box.asm</code>) that interfaces with the screen memory map and keyboard to render and erase a black rectangular box in real-time.",
        body_style
    ))

    # K Parameters Table
    k_data = [
        [Paragraph("<b>Parameter Metric</b>", body_style), Paragraph("<b>Mathematical Formula</b>", body_style), Paragraph("<b>Derived Value for K = 52</b>", body_style)],
        [Paragraph("Personal Number (K)", body_style), Paragraph("Roll No mod 100", body_style), Paragraph("<b>52</b>", body_style)],
        [Paragraph("Assembler Extra Feature", body_style), Paragraph("K mod 3", body_style), Paragraph("<b>52 mod 3 = 1</b> (Line-numbered syntax error reporting)", body_style)],
        [Paragraph("Words per Screen Row", body_style), Paragraph("(K mod 4) + 1", body_style), Paragraph("<b>(52 mod 4) + 1 = 1 word</b> (16-bit)", body_style)],
        [Paragraph("Box Pixel Width", body_style), Paragraph("16 × ((K mod 4) + 1)", body_style), Paragraph("<b>16 pixels</b>", body_style)],
        [Paragraph("Box Starting Row", body_style), Paragraph("Row K", body_style), Paragraph("<b>Row 52</b> (from top edge)", body_style)],
        [Paragraph("Box Height", body_style), Paragraph("Fixed specification", body_style), Paragraph("<b>20 screen rows</b> (Rows 52 to 71)", body_style)],
        [Paragraph("Screen Base Address", body_style), Paragraph("SCREEN + 32 × K", body_style), Paragraph("<b>16384 + (32 × 52) = 18048</b> (0x4680)", body_style)],
        [Paragraph("Screen Ending Address", body_style), Paragraph("Base + 32 × 19", body_style), Paragraph("<b>18048 + 608 = 18656</b>", body_style)]
    ]
    t_k = Table(k_data, colWidths=[130, 150, 204])
    t_k.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0B2545")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#94A3B8")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_k)
    story.append(Spacer(1, 8))

    # ==========================================
    # SECTION 2: PART A - HACK COMPUTER IMPLEMENTATION
    # ==========================================
    story.append(Paragraph("2. Part A – Hack Computer HDL Hardware Architecture", h1_style))
    story.append(Paragraph(
        "The Hack Computer is constructed using three primary interconnected HDL chips: "
        "<code>CPU.hdl</code>, <code>Memory.hdl</code>, and <code>Computer.hdl</code>.",
        body_style
    ))

    story.append(Paragraph("2.1 Central Processing Unit (CPU.hdl)", h2_style))
    story.append(Paragraph(
        "The Hack CPU decodes 16-bit instructions, performs arithmetic/logic computations via the ALU, and manages control flow: "
        "<br/>• <b>A-Instruction (bit 15 = 0):</b> Loads the 15-bit address or constant into the A register. "
        "<br/>• <b>C-Instruction (bit 15 = 1):</b> The instruction format is <code>111 a cccccc ddd jjj</code>. "
        "The ALU operates on <code>x = outD</code> and <code>y = Mux16(outA, inM, sel=a)</code>. "
        "Destination bits control loading into A (d1), D (d2), and memory (d3). "
        "<br/>• <b>Jump Logic (PC):</b> Condition flags are tested: <code>jlt = j1 & ng</code>, <code>jeq = j2 & zr</code>, <code>jgt = j3 & !(zr | ng)</code>. "
        "When satisfied, <code>loadPC = 1</code> vectors PC to the address in A; otherwise <code>inc = 1</code> advances PC sequentially.",
        body_style
    ))

    with open(r"C:\Nand and tetris\capstone\CPU.hdl", "r") as f:
        cpu_code = f.read()
    story.append(Preformatted(cpu_code, code_style))

    story.append(Paragraph("2.2 Memory Architecture (Memory.hdl)", h2_style))
    story.append(Paragraph(
        "The Hack address space spans 32K memory words, partitioned as: "
        "<br/>• <b>RAM16K (0 to 16383 / 0x0000 - 0x3FFF):</b> Selected when <code>address[14] == 0</code>. "
        "<br/>• <b>Screen (16384 to 24575 / 0x4000 - 0x5FFF):</b> Memory-mapped screen bitmap when <code>address[14..13] == 10</code>. "
        "<br/>• <b>Keyboard (24576 / 0x6000):</b> Dedicated input register when <code>address[14..13] == 11</code>.",
        body_style
    ))

    with open(r"C:\Nand and tetris\capstone\Memory.hdl", "r") as f:
        mem_code = f.read()
    story.append(Preformatted(mem_code, code_style))

    story.append(Paragraph("2.3 Top-Level Computer Integration (Computer.hdl)", h2_style))
    story.append(Paragraph(
        "<code>Computer.hdl</code> integrates <code>ROM32K</code>, <code>CPU</code>, and <code>Memory</code> into a closed system loop. "
        "When <code>reset == 1</code>, execution restarts from ROM address 0.",
        body_style
    ))

    with open(r"C:\Nand and tetris\capstone\Computer.hdl", "r") as f:
        comp_code = f.read()
    story.append(Preformatted(comp_code, code_style))

    story.append(PageBreak())

    # ==========================================
    # SECTION 3: PART B - PYTHON ASSEMBLER
    # ==========================================
    story.append(Paragraph("3. Part B – Two-Pass Python Assembler (assembler.py)", h1_style))
    story.append(Paragraph(
        "The Python assembler implements the classic two-pass translation pipeline: "
        "<br/>• <b>First Pass (Symbol Table & Label Resolution):</b> Strips comments and whitespace, tracks ROM instruction addresses, "
        "and binds label declarations like <code>(MAIN_LOOP)</code> to the target ROM address without generating machine code words. "
        "<br/>• <b>Second Pass (Code Generation & Variable Allocation):</b> Translates A-instructions and C-instructions. "
        "Unseen variables are allocated consecutive RAM addresses starting from address 16 ($16, 17, 18, \dots$). "
        "<br/>• <b>Personal Feature for K = 52 (K mod 3 = 1):</b> The assembler catches syntax errors and outputs line-specific diagnostics "
        "(e.g., <code>Line 3: invalid instruction</code>) rather than crashing unhandled. In addition, symbol tables are cleanly exported to <code>symbols.txt</code>.",
        body_style
    ))

    # Assembler Core Methods Excerpt
    asm_core_excerpt = '''class HackAssembler:
    def first_pass(self, lines):
        rom_address = 0
        for line_num, raw_line in enumerate(lines, start=1):
            cleaned = self.clean_line(raw_line)
            if not cleaned: continue
            if cleaned.startswith('(') and cleaned.endswith(')'):
                label = cleaned[1:-1].strip()
                self.symbol_table[label] = rom_address
            else:
                self.clean_instructions.append((line_num, cleaned))
                rom_address += 1

    def second_pass(self):
        binary_code = []
        for line_num, inst in self.clean_instructions:
            try:
                if inst.startswith('@'):
                    bin_inst = self.parse_a_instruction(inst, line_num)
                else:
                    bin_inst = self.parse_c_instruction(inst, line_num)
                binary_code.append(bin_inst)
            except Exception as err:
                # K mod 3 == 1: Clear error message with line number
                error_msg = f"Line {line_num}: invalid instruction ({err})"
                self.errors.append(error_msg)
                print(error_msg)
        return binary_code'''
    story.append(Preformatted(asm_core_excerpt, code_style))

    # ==========================================
    # SECTION 4: PART C - BOX PROGRAM
    # ==========================================
    story.append(Paragraph("4. Part C – Box Assembly Program (Box.asm)", h1_style))
    story.append(Paragraph(
        "<b>Box.asm</b> operates as a real-time reactive device driver: "
        "<br/>1. <b>Keyboard Polling:</b> Reads memory-mapped location 24576 (<code>@KBD</code>). "
        "<br/>2. <b>Color Logic:</b> If <code>RAM[KBD] != 0</code>, sets <code>color = -1</code> (0xFFFF, black); otherwise sets <code>color = 0</code> (white). "
        "<br/>3. <b>Screen Rasterization:</b> Begins at base address <b>18048</b> ($16384 + 32 \times 52$). For each of the 20 rows, "
        "writes <code>color</code> into word 0, adds 32 to advance to the next screen row (<code>M=D+M</code>), and decrements <code>row_count</code>.",
        body_style
    ))

    with open(r"C:\Nand and tetris\capstone\Box.asm", "r") as f:
        box_code = f.read()
    story.append(Preformatted(box_code, code_style))

    story.append(Paragraph("Assembled Machine Code Output (Box.hack - First 16 Words):", h2_style))
    with open(r"C:\Nand and tetris\capstone\Box.hack", "r") as f:
        hack_lines = [l.strip() for l in f if l.strip()][:16]
    hack_display = "\n".join([f"ROM[{i:02d}]: {l}" for i, l in enumerate(hack_lines)])
    story.append(Preformatted(hack_display, code_style))

    story.append(PageBreak())

    # ==========================================
    # SECTION 5: VERIFICATION & CPU SIMULATION
    # ==========================================
    story.append(Paragraph("5. Systematic Verification & CPU Execution Results", h1_style))
    story.append(Paragraph(
        "The implementation was verified using official test scripts and cycle-accurate Hack CPU simulation:",
        body_style
    ))

    # Test Results Table
    test_results_data = [
        [Paragraph("<b>Component Tested</b>", body_style), Paragraph("<b>Test Benchmark</b>", body_style), Paragraph("<b>Expected Behavior</b>", body_style), Paragraph("<b>Status</b>", body_style)],
        [Paragraph("Hack CPU (CPU.hdl)", body_style), Paragraph("CPU.tst / CPU.cmp", body_style), Paragraph("Exact register, ALU, PC matches", body_style), Paragraph("<font color='#16A34A'><b>PASSED</b></font>", body_style)],
        [Paragraph("Memory (Memory.hdl)", body_style), Paragraph("Memory.tst / Memory.cmp", body_style), Paragraph("RAM16K, Screen, KBD addressing", body_style), Paragraph("<font color='#16A34A'><b>PASSED</b></font>", body_style)],
        [Paragraph("Computer (Computer.hdl)", body_style), Paragraph("ComputerAdd.tst", body_style), Paragraph("D register computes R0 = 2+3 = 5", body_style), Paragraph("<font color='#16A34A'><b>PASSED</b></font>", body_style)],
        [Paragraph("Python Assembler", body_style), Paragraph("Add.asm to Add.hack", body_style), Paragraph("100% bit-exact match with official hack", body_style), Paragraph("<font color='#16A34A'><b>PASSED</b></font>", body_style)],
        [Paragraph("Extra Feature (K mod 3=1)", body_style), Paragraph("Bad.asm syntax test", body_style), Paragraph("Line 3: invalid instruction reported", body_style), Paragraph("<font color='#16A34A'><b>PASSED</b></font>", body_style)],
        [Paragraph("Box Drawing (Key Down)", body_style), Paragraph("RAM[KBD] = 65 ('A')", body_style), Paragraph("RAM[18048..18656] set to -1 (Black)", body_style), Paragraph("<font color='#16A34A'><b>PASSED</b></font>", body_style)],
        [Paragraph("Box Erase (Key Up)", body_style), Paragraph("RAM[KBD] = 0", body_style), Paragraph("RAM[18048..18656] set to 0 (White)", body_style), Paragraph("<font color='#16A34A'><b>PASSED</b></font>", body_style)],
    ]
    t_results = Table(test_results_data, colWidths=[120, 110, 190, 64])
    t_results.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0B2545")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_results)
    story.append(Spacer(1, 10))

    story.append(Paragraph("Visual Rasterization of Drawn Box (First 5 of 20 Rows on Screen):", h2_style))
    raster_ascii = (
        "Screen Coordinates: Top-Left (Row 52, Word 0) -> 16 pixels wide x 20 rows tall\n"
        "----------------------------------------------------------------------------------\n"
        "Row 52 (RAM[18048]): [================] (Word 0: Black) | (Remaining 31 words: White)\n"
        "Row 53 (RAM[18080]): [================] (Word 0: Black) | (Remaining 31 words: White)\n"
        "Row 54 (RAM[18112]): [================] (Word 0: Black) | (Remaining 31 words: White)\n"
        "Row 55 (RAM[18144]): [================] (Word 0: Black) | (Remaining 31 words: White)\n"
        "Row 56 (RAM[18176]): [================] (Word 0: Black) | (Remaining 31 words: White)\n"
        "       ... (Repeats for all 20 consecutive rows up to Row 71 / RAM[18656]) ..."
    )
    story.append(Preformatted(raster_ascii, code_style))
    story.append(Spacer(1, 10))

    # ==========================================
    # SECTION 6: DEBUGGING & VIVA PREPARATION
    # ==========================================
    story.append(Paragraph("6. Programming Mistake Encountered & Technical Viva Answers", h1_style))
    story.append(Paragraph(
        "<b>Debugging Case Study:</b><br/>"
        "• <i>Encountered Error:</i> The instruction <code>M=M+D</code> triggered an assembler error: <code>Invalid comp expression 'M+D'</code>.<br/>"
        "• <i>Analysis:</i> The Hack ALU hardware controls specify arithmetic addition as $D+A$ or $D+M$. The Hack assembly specification requires $D$ as the left operand.<br/>"
        "• <i>Resolution:</i> Corrected <code>Box.asm</code> to <code>M=D+M</code> and expanded <code>assembler.py</code> to support commutative operand orders.",
        body_style
    ))
    story.append(Spacer(1, 6))

    story.append(Paragraph("Viva Voce Key Questions & Answers:", h2_style))
    viva_qa = [
        "<b>Q1: How does CPU.hdl control program execution?</b><br/>"
        "A: Bit 15 switches between constant loading (A-instruction) and computation (C-instruction). ALU zero and negative flags (zr, ng) are combined with jump bits (j1, j2, j3) to conditionally assert loadPC.",
        
        "<b>Q2: How does Hack Screen Memory mapping work?</b><br/>"
        "A: The screen is a 512x256 monochrome matrix mapped from 16384 to 24575. Each row has 32 16-bit words. Row r starts at <code>16384 + 32*r</code>. Setting a word to -1 turns 16 pixels black; 0 turns them white.",
        
        "<b>Q3: How to make live on-the-spot modifications during the viva?</b><br/>"
        "• <i>Move box down by 10 rows:</i> Change starting row address from <code>@18048</code> to <code>@18368</code> (since 18048 + 32*10 = 18368).<br/>"
        "• <i>Change box height to 30 rows:</i> Change <code>@20</code> to <code>@30</code> at row counter initialization.<br/>"
        "• <i>Change box width to 32 pixels:</i> Add <code>A=A+1; M=D</code> after Word 0 inside the drawing loop."
    ]
    for qa in viva_qa:
        story.append(Paragraph(qa, body_style))
        story.append(Spacer(1, 3))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF successfully built: {pdf_filename}")

if __name__ == '__main__':
    build_pdf()
