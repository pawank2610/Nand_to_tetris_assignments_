#!/usr/bin/env python3
"""
Hack Assembler with Invalid Instruction Error Handling (Personal Number K = 52, K mod 3 = 1)
Course: ETCNTC301 - Nand to Tetris - I
School of Engineering & Technology, K.R. Mangalam University
Student Name: Pawan Kr. Singh
Roll Number: 2501730252
Personal Number K = 52 (52 mod 3 = 1 -> Invalid Instruction Line Error Handling)
"""

import sys
import os
import re

PREDEFINED_SYMBOLS = {
    "SP": 0, "LCL": 1, "ARG": 2, "THIS": 3, "THAT": 4,
    "SCREEN": 16384, "KBD": 24576
}
for i in range(16):
    PREDEFINED_SYMBOLS[f"R{i}"] = i

COMP_TABLE = {
    "0": "0101010", "1": "0111111", "-1": "0111010",
    "D": "0001100", "A": "0110000", "!D": "0001101",
    "!A": "0110001", "-D": "0001111", "-A": "0110011",
    "D+1": "0011111", "A+1": "0110111", "D-1": "0001110",
    "A-1": "0110010", "D+A": "0000010", "D-A": "0010011",
    "A-D": "0000111", "D&A": "0000000", "D|A": "0010101",
    "M": "1110000", "!M": "1110001", "-M": "1110011",
    "M+1": "1110111", "M-1": "1110010", "D+M": "1000010",
    "D-M": "1010011", "M-D": "1000111", "D&M": "1000000",
    "D|M": "1010101"
}

DEST_TABLE = {
    "": "000", "M": "001", "D": "010", "MD": "011",
    "A": "100", "AM": "101", "AD": "110", "AMD": "111"
}

JUMP_TABLE = {
    "": "000", "JGT": "001", "JEQ": "010", "JGE": "011",
    "JLT": "100", "JNE": "101", "JLE": "110", "JMP": "111"
}

SYMBOL_REGEX = re.compile(r"^[a-zA-Z_.$:][a-zA-Z0-9_.$:]*$")

class AssemblyError(Exception):
    def __init__(self, line_num, message="invalid instruction"):
        self.line_num = line_num
        self.message = message
        super().__init__(f"Line {line_num}: {message}")

class HackAssembler:
    def __init__(self):
        self.symbol_table = {}
        self.next_var_address = 16
        self.num_labels = 0
        self.num_variables = 0

    def assemble(self, asm_source_lines):
        self.symbol_table = dict(PREDEFINED_SYMBOLS)
        self.next_var_address = 16
        self.num_labels = 0
        self.num_variables = 0

        rom_address = 0
        cleaned_instructions = []

        # PASS 1: Labels & Symbol Resolution
        for line_idx, raw_line in enumerate(asm_source_lines):
            line_num = line_idx + 1
            cleaned = raw_line.split("//")[0].strip()
            if not cleaned:
                continue

            if cleaned.startswith("("):
                if not cleaned.endswith(")"):
                    raise AssemblyError(line_num, "invalid instruction")
                label = cleaned[1:-1].strip()
                if not label or not SYMBOL_REGEX.match(label):
                    raise AssemblyError(line_num, "invalid instruction")
                if label in self.symbol_table:
                    raise AssemblyError(line_num, "invalid instruction")
                self.symbol_table[label] = rom_address
                self.num_labels += 1
            else:
                cleaned_instructions.append((line_num, cleaned))
                rom_address += 1

        # PASS 2: Binary Code Translation
        binary_code = []
        for line_num, inst in cleaned_instructions:
            if inst.startswith("@"):
                val_str = inst[1:].strip()
                if not val_str:
                    raise AssemblyError(line_num, "invalid instruction")
                if val_str.isdigit():
                    val = int(val_str)
                    if val < 0 or val > 32767:
                        raise AssemblyError(line_num, "invalid instruction")
                elif SYMBOL_REGEX.match(val_str):
                    if val_str not in self.symbol_table:
                        self.symbol_table[val_str] = self.next_var_address
                        self.next_var_address += 1
                        self.num_variables += 1
                    val = self.symbol_table[val_str]
                else:
                    raise AssemblyError(line_num, "invalid instruction")
                binary_code.append(f"0{val:015b}")
            else:
                s = "".join(inst.split())
                dest_part, jump_part, comp_part = "", "", ""
                if "=" in s:
                    dest_part, s = s.split("=", 1)
                if ";" in s:
                    comp_part, jump_part = s.split(";", 1)
                else:
                    comp_part = s

                if dest_part not in DEST_TABLE:
                    raise AssemblyError(line_num, "invalid instruction")
                if comp_part not in COMP_TABLE:
                    raise AssemblyError(line_num, "invalid instruction")
                if jump_part not in JUMP_TABLE:
                    raise AssemblyError(line_num, "invalid instruction")

                comp_bin = COMP_TABLE[comp_part]
                dest_bin = DEST_TABLE[dest_part]
                jump_bin = JUMP_TABLE[jump_part]
                binary_code.append(f"111{comp_bin}{dest_bin}{jump_bin}")

        return binary_code

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 assembler.py <input.asm> [output.hack]")
        sys.exit(1)

    input_path = sys.argv[1]
    if len(sys.argv) >= 3:
        output_path = sys.argv[2]
    else:
        base, _ = os.path.splitext(input_path)
        output_path = f"{base}.hack"

    if not os.path.exists(input_path):
        print(f"Error: file not found '{input_path}'", file=sys.stderr)
        sys.exit(1)

    with open(input_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    assembler = HackAssembler()
    try:
        binary_output = assembler.assemble(lines)
    except AssemblyError as e:
        print(str(e), file=sys.stderr)
        if os.path.exists(output_path):
            try: os.remove(output_path)
            except OSError: pass
        sys.exit(1)
    except Exception:
        print("invalid instruction", file=sys.stderr)
        sys.exit(1)

    with open(output_path, "w", encoding="utf-8") as f:
        for code in binary_output:
            f.write(code + "\n")

    print("=== Hack Assembly Successful ===")
    print("Personal Number (K):    52")
    print("Student Parameter K:    52 (Roll: 2501730252 - Pawan Kr. Singh)")
    print(f"Input file:             {input_path}")
    print(f"Output file:            {output_path}")
    print(f"Instructions assembled: {len(binary_output)}")
    print(f"Labels defined:         {assembler.num_labels}")
    print(f"Variables allocated:    {assembler.num_variables}")
    print("Status:                 SUCCESS (52)")

if __name__ == "__main__":
    main()
