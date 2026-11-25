#!/usr/bin/env python3
"""
Unit Test Suite for Hack Assembler
Author: Bhavya Anand (Roll No: 2501730046, K = 46)
Course: Nand to Tetris – I (ETCNTC301)
University: K.R. Mangalam University

Verifies:
- Standard benchmark translation vs official reference files (Add, Max, Rect, Pong)
- Predefined symbols (SP, LCL, ARG, THIS, THAT, R0-R15, SCREEN, KBD)
- Label resolution (Pass 1)
- RAM variable allocation starting at RAM address 16
- Error handling with original line numbers (Feature for K mod 3 = 1):
  - Invalid destination (e.g. X=D)
  - Invalid computation (e.g. D=X)
  - Invalid jump (e.g. D;FOO)
  - Invalid symbols / malformed A-instructions (e.g. @VAR!, @-1, @32768)
  - Malformed labels (e.g. (123), (LABEL!)
  - Duplicate labels
"""

import unittest
import os
import sys
import tempfile
import subprocess

# Add assembler directory to sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSEMBLER_DIR = os.path.join(BASE_DIR, "assembler")
sys.path.insert(0, ASSEMBLER_DIR)

from assembler import HackAssembler, AssemblyError


class TestHackAssemblerBenchmarks(unittest.TestCase):
    def setUp(self):
        self.assembler = HackAssembler()

    def _compare_with_reference(self, asm_name, ref_name):
        asm_path = os.path.join(ASSEMBLER_DIR, asm_name)
        ref_path = os.path.join(ASSEMBLER_DIR, ref_name)
        with open(asm_path, "r") as f:
            asm_lines = f.readlines()
        with open(ref_path, "r") as f:
            ref_lines = [line.strip() for line in f if line.strip()]

        assembled = self.assembler.assemble(asm_lines)
        self.assertEqual(len(assembled), len(ref_lines), f"Instruction count mismatch for {asm_name}")
        for i, (out_line, ref_line) in enumerate(zip(assembled, ref_lines)):
            self.assertEqual(out_line, ref_line, f"Mismatch at instruction {i} in {asm_name}")

    def test_add_benchmark(self):
        self._compare_with_reference("Add.asm", "Add.ref.hack")

    def test_max_benchmark(self):
        self._compare_with_reference("Max.asm", "Max.ref.hack")

    def test_rect_benchmark(self):
        self._compare_with_reference("Rect.asm", "Rect.ref.hack")

    def test_pong_benchmark(self):
        self._compare_with_reference("Pong.asm", "Pong.ref.hack")


class TestSymbolResolution(unittest.TestCase):
    def setUp(self):
        self.assembler = HackAssembler()

    def test_predefined_symbols(self):
        asm_code = [
            "@SCREEN\n",
            "@KBD\n",
            "@SP\n",
            "@LCL\n",
            "@ARG\n",
            "@THIS\n",
            "@THAT\n",
            "@R0\n",
            "@R15\n"
        ]
        out = self.assembler.assemble(asm_code)
        self.assertEqual(out[0], f"0{16384:015b}")
        self.assertEqual(out[1], f"0{24576:015b}")
        self.assertEqual(out[2], f"0{0:015b}")
        self.assertEqual(out[3], f"0{1:015b}")
        self.assertEqual(out[4], f"0{2:015b}")
        self.assertEqual(out[5], f"0{3:015b}")
        self.assertEqual(out[6], f"0{4:015b}")
        self.assertEqual(out[7], f"0{0:015b}")
        self.assertEqual(out[8], f"0{15:015b}")

    def test_variable_allocation_from_16(self):
        asm_code = [
            "@counter\n",  # Should get 16
            "@i\n",        # Should get 17
            "@counter\n",  # Should reuse 16
            "@sum\n",      # Should get 18
            "@i\n"         # Should reuse 17
        ]
        out = self.assembler.assemble(asm_code)
        self.assertEqual(out[0], f"0{16:015b}")
        self.assertEqual(out[1], f"0{17:015b}")
        self.assertEqual(out[2], f"0{16:015b}")
        self.assertEqual(out[3], f"0{18:015b}")
        self.assertEqual(out[4], f"0{17:015b}")

    def test_labels_resolution(self):
        asm_code = [
            "// Simple loop\n",
            "(LOOP)\n",
            "@LOOP\n",
            "0;JMP\n",
            "(END)\n",
            "@END\n",
            "0;JMP\n"
        ]
        out = self.assembler.assemble(asm_code)
        # LOOP is at ROM address 0
        self.assertEqual(out[0], f"0{0:015b}")
        self.assertEqual(out[1], "1110101010000111")  # 0;JMP
        # END is at ROM address 2
        self.assertEqual(out[2], f"0{2:015b}")
        self.assertEqual(out[3], "1110101010000111")  # 0;JMP


class TestInvalidInstructionErrorHandling(unittest.TestCase):
    """
    K = 46 -> K mod 3 = 1: Invalid instruction error handling with line numbers.
    Tests verify that invalid syntax produces the expected message and non-zero exit code.
    """
    def setUp(self):
        self.assembler = HackAssembler()

    def test_invalid_computation_line_number(self):
        asm_code = [
            "// Line 1\n",
            "@R0\n",      # Line 2
            "D=M\n",      # Line 3
            "// Line 4\n",
            "D=X\n",      # Line 5: INVALID comp
            "@R1\n"
        ]
        with self.assertRaises(AssemblyError) as ctx:
            self.assembler.assemble(asm_code)
        self.assertEqual(ctx.exception.line_num, 5)
        self.assertEqual(str(ctx.exception), "Line 5: invalid instruction")

    def test_invalid_destination_line_number(self):
        asm_code = [
            "@R0\n",
            "XYZ=D\n"    # Line 2: INVALID dest
        ]
        with self.assertRaises(AssemblyError) as ctx:
            self.assembler.assemble(asm_code)
        self.assertEqual(ctx.exception.line_num, 2)
        self.assertEqual(str(ctx.exception), "Line 2: invalid instruction")

    def test_invalid_jump_line_number(self):
        asm_code = [
            "@R0\n",      # Line 1
            "D=A\n",      # Line 2
            "D;JUMPFAST\n"# Line 3: INVALID jump
        ]
        with self.assertRaises(AssemblyError) as ctx:
            self.assembler.assemble(asm_code)
        self.assertEqual(ctx.exception.line_num, 3)
        self.assertEqual(str(ctx.exception), "Line 3: invalid instruction")

    def test_invalid_a_instruction_symbol(self):
        asm_code = [
            "// Comments\n",                     # Line 1
            "\n",                                # Line 2
            "@VALID_SYMBOL\n",                   # Line 3
            "@INVALID_SYMBOL_WITH_SYNTAX!\n"     # Line 4: INVALID symbol
        ]
        with self.assertRaises(AssemblyError) as ctx:
            self.assembler.assemble(asm_code)
        self.assertEqual(ctx.exception.line_num, 4)
        self.assertEqual(str(ctx.exception), "Line 4: invalid instruction")

    def test_invalid_a_instruction_constant_out_of_range(self):
        asm_code = [
            "@32768\n"   # Line 1: Exceeds 15-bit address limit (0..32767)
        ]
        with self.assertRaises(AssemblyError) as ctx:
            self.assembler.assemble(asm_code)
        self.assertEqual(ctx.exception.line_num, 1)
        self.assertEqual(str(ctx.exception), "Line 1: invalid instruction")

    def test_invalid_a_instruction_negative(self):
        asm_code = [
            "@-5\n"      # Line 1: Negative number invalid for @
        ]
        with self.assertRaises(AssemblyError) as ctx:
            self.assembler.assemble(asm_code)
        self.assertEqual(ctx.exception.line_num, 1)
        self.assertEqual(str(ctx.exception), "Line 1: invalid instruction")

    def test_malformed_label(self):
        asm_code = [
            "// Header\n",
            "(123_INVALID)\n"  # Line 2: Label cannot start with digit
        ]
        with self.assertRaises(AssemblyError) as ctx:
            self.assembler.assemble(asm_code)
        self.assertEqual(ctx.exception.line_num, 2)
        self.assertEqual(str(ctx.exception), "Line 2: invalid instruction")

    def test_duplicate_label(self):
        asm_code = [
            "(LOOP)\n",    # Line 1
            "@R0\n",       # Line 2
            "(LOOP)\n"     # Line 3: Duplicate label definition
        ]
        with self.assertRaises(AssemblyError) as ctx:
            self.assembler.assemble(asm_code)
        self.assertEqual(ctx.exception.line_num, 3)
        self.assertEqual(str(ctx.exception), "Line 3: invalid instruction")

    def test_cli_execution_with_invalid_instruction(self):
        """Verify command-line execution returns non-zero exit code and outputs Line N: invalid instruction."""
        with tempfile.NamedTemporaryFile("w", suffix=".asm", delete=False) as tf:
            tf.write("// Header\n@R0\nD=M\n// Line 4\n// Line 5\n// Line 6\nD=X\n")
            temp_path = tf.name

        try:
            cmd = [sys.executable, os.path.join(ASSEMBLER_DIR, "assembler.py"), temp_path]
            proc = subprocess.run(cmd, capture_output=True, text=True)
            self.assertNotEqual(proc.returncode, 0, "Assembler should exit with non-zero on invalid instruction")
            self.assertIn("Line 7: invalid instruction", proc.stderr)
            # Verify no .hack was generated
            hack_path = temp_path.replace(".asm", ".hack")
            self.assertFalse(os.path.exists(hack_path), "No .hack file should be created for invalid assembly")
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)


if __name__ == "__main__":
    unittest.main()
