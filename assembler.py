"""
Hack Assembler for Nand to Tetris - I (ETCNTC301)
School of Engineering & Technology, K.R. Mangalam University
Author: Capstone Implementation

Usage:
    python assembler.py <file.asm> [K]
Example:
    python assembler.py Box.asm 41
"""

import sys
import os

# Predefined Symbols in Hack Platform
PREDEFINED_SYMBOLS = {
    'SP': 0, 'LCL': 1, 'ARG': 2, 'THIS': 3, 'THAT': 4,
    'SCREEN': 16384, 'KBD': 24576,
    'R0': 0, 'R1': 1, 'R2': 2, 'R3': 3,
    'R4': 4, 'R5': 5, 'R6': 6, 'R7': 7,
    'R8': 8, 'R9': 9, 'R10': 10, 'R11': 11,
    'R12': 12, 'R13': 13, 'R14': 14, 'R15': 15
}

# Computation specifications (a c1 c2 c3 c4 c5 c6)
COMP_TABLE = {
    # When a = 0 (ALU operates on D and A)
    '0':   '0101010',
    '1':   '0111111',
    '-1':  '0111010',
    'D':   '0001100',
    'A':   '0110000',
    '!D':  '0001101',
    '!A':  '0110001',
    '-D':  '0001111',
    '-A':  '0110011',
    'D+1': '0011111',
    'A+1': '0110111',
    'D-1': '0001110',
    'A-1': '0110010',
    'D+A': '0000010',
    'D-A': '0010011',
    'A-D': '0000111',
    'D&A': '0000000',
    'D|A': '0010101',
    # When a = 1 (ALU operates on D and M)
    'M':   '1110000',
    '!M':  '1110001',
    '-M':  '1110011',
    'M+1': '1110111',
    'M-1': '1110010',
    'D+M': '1000010',
    'M+D': '1000010',
    'D-M': '1010011',
    'M-D': '1000111',
    'D&M': '1000000',
    'M&D': '1000000',
    'D|M': '1010101',
    'M|D': '1010101',
}

# Destination specifications (d1 d2 d3)
DEST_TABLE = {
    '':    '000',
    'M':   '001',
    'D':   '010',
    'MD':  '011',
    'DM':  '011',
    'A':   '100',
    'AM':  '101',
    'AD':  '110',
    'AMD': '111'
}

# Jump specifications (j1 j2 j3)
JUMP_TABLE = {
    '':    '000',
    'JGT': '001',
    'JEQ': '010',
    'JGE': '011',
    'JLT': '100',
    'JNE': '101',
    'JLE': '110',
    'JMP': '111'
}


class HackAssembler:
    def __init__(self, k=None):
        self.k = k
        self.symbol_table = dict(PREDEFINED_SYMBOLS)
        self.next_variable_address = 16
        self.raw_lines = []
        self.clean_instructions = []  # list of (original_line_num, instruction_text)
        self.labels = {}
        self.variables = {}
        self.errors = []
        self.warnings = []

    def clean_line(self, line):
        """Strip comments and surrounding whitespace."""
        idx = line.find('//')
        if idx != -1:
            line = line[:idx]
        return line.strip()

    def first_pass(self, lines):
        """
        First Pass: Read assembly, strip comments and whitespace,
        record labels (LOOP) and their ROM addresses.
        Feature K mod 3 == 2: Warn if label is written twice.
        """
        rom_address = 0
        seen_labels = set()

        for line_num, raw_line in enumerate(lines, start=1):
            cleaned = self.clean_line(raw_line)
            if not cleaned:
                continue

            if cleaned.startswith('(') and cleaned.endswith(')'):
                label = cleaned[1:-1].strip()
                if not label:
                    self.errors.append(f"Line {line_num}: Empty label '()'")
                    continue

                if label in seen_labels:
                    warning_msg = f"Warning: Duplicate label '({label})' at line {line_num}"
                    self.warnings.append(warning_msg)
                    print(warning_msg)
                else:
                    seen_labels.add(label)

                self.symbol_table[label] = rom_address
                self.labels[label] = rom_address
            else:
                self.clean_instructions.append((line_num, cleaned))
                rom_address += 1

    def parse_a_instruction(self, instruction, line_num):
        """Parse @value or @symbol to 16-bit binary."""
        symbol = instruction[1:].strip()
        if not symbol:
            raise ValueError(f"Line {line_num}: Invalid empty A-instruction '@'")

        if symbol.isdigit():
            address = int(symbol)
            if address > 32767:
                raise ValueError(f"Line {line_num}: Constant @{address} exceeds 15-bit address space")
        else:
            if symbol not in self.symbol_table:
                # Assign next RAM address to new variable
                self.symbol_table[symbol] = self.next_variable_address
                self.variables[symbol] = self.next_variable_address
                self.next_variable_address += 1
            address = self.symbol_table[symbol]

        return format(address, '016b')

    def parse_c_instruction(self, instruction, line_num):
        """Parse dest=comp;jump to 16-bit binary (111accccccdddjjj)."""
        dest_part = ""
        comp_part = instruction
        jump_part = ""

        if ';' in comp_part:
            comp_part, jump_part = comp_part.split(';', 1)
            jump_part = jump_part.strip()

        if '=' in comp_part:
            dest_part, comp_part = comp_part.split('=', 1)
            dest_part = dest_part.strip()

        comp_part = comp_part.strip()

        if comp_part not in COMP_TABLE:
            raise ValueError(f"Line {line_num}: Invalid comp expression '{comp_part}' in '{instruction}'")
        if dest_part not in DEST_TABLE:
            raise ValueError(f"Line {line_num}: Invalid dest expression '{dest_part}' in '{instruction}'")
        if jump_part not in JUMP_TABLE:
            raise ValueError(f"Line {line_num}: Invalid jump expression '{jump_part}' in '{instruction}'")

        comp_bits = COMP_TABLE[comp_part]
        dest_bits = DEST_TABLE[dest_part]
        jump_bits = JUMP_TABLE[jump_part]

        return f"111{comp_bits}{dest_bits}{jump_bits}"

    def second_pass(self):
        """
        Second Pass: Convert clean instructions into 16-bit binary code.
        Feature K mod 3 == 1: Catch incorrect instructions and print line-specific error.
        """
        binary_code = []

        for line_num, inst in self.clean_instructions:
            try:
                if inst.startswith('@'):
                    bin_inst = self.parse_a_instruction(inst, line_num)
                else:
                    bin_inst = self.parse_c_instruction(inst, line_num)
                binary_code.append(bin_inst)
            except Exception as err:
                error_msg = f"Line {line_num}: invalid instruction ({err})"
                self.errors.append(error_msg)
                print(error_msg)

        return binary_code

    def save_symbols_file(self, output_path="symbols.txt"):
        """
        Feature K mod 3 == 0: Save all labels and variables with their addresses.
        """
        with open(output_path, 'w') as f:
            f.write("==================================================\n")
            f.write(" Hack Assembler Symbol Table Export\n")
            f.write(f" Student Personal Number K: {self.k}\n")
            f.write("==================================================\n\n")

            f.write("[LABELS (ROM Addresses)]:\n")
            f.write(f"{'Label Name':<25} {'ROM Address (Dec)':<20} {'ROM Address (Hex)'}\n")
            f.write("-" * 65 + "\n")
            for label, addr in sorted(self.labels.items(), key=lambda x: x[1]):
                f.write(f"{label:<25} {addr:<20} 0x{addr:04X}\n")

            f.write("\n[USER VARIABLES (RAM Addresses starting from 16)]:\n")
            f.write(f"{'Variable Name':<25} {'RAM Address (Dec)':<20} {'RAM Address (Hex)'}\n")
            f.write("-" * 65 + "\n")
            for var, addr in sorted(self.variables.items(), key=lambda x: x[1]):
                f.write(f"{var:<25} {addr:<20} 0x{addr:04X}\n")

            f.write("\n[PREDEFINED SYMBOLS]:\n")
            f.write(f"{'Symbol Name':<25} {'Address (Dec)':<20} {'Address (Hex)'}\n")
            f.write("-" * 65 + "\n")
            for sym, addr in sorted(PREDEFINED_SYMBOLS.items(), key=lambda x: x[1]):
                f.write(f"{sym:<25} {addr:<20} 0x{addr:04X}\n")

    def assemble(self, asm_file_path, output_hack_path=None):
        """Assemble .asm file into .hack file."""
        if not os.path.exists(asm_file_path):
            raise FileNotFoundError(f"Input file '{asm_file_path}' not found.")

        with open(asm_file_path, 'r') as f:
            lines = f.readlines()

        # Step 1: First Pass
        self.first_pass(lines)

        # Step 2: Second Pass
        binary_code = self.second_pass()

        if self.errors:
            print(f"Assembly completed with {len(self.errors)} error(s).")
            # For K mod 3 == 1, clear error message has been printed.
            if not binary_code:
                return False

        # Output Hack file
        if not output_hack_path:
            base, _ = os.path.splitext(asm_file_path)
            output_hack_path = base + ".hack"

        with open(output_hack_path, 'w') as f:
            for b in binary_code:
                f.write(b + "\n")

        print(f"Successfully generated: {output_hack_path} ({len(binary_code)} instructions)")

        # Feature K mod 3 == 0 (or if requested/configured)
        symbols_path = os.path.join(os.path.dirname(output_hack_path) or ".", "symbols.txt")
        self.save_symbols_file(symbols_path)
        print(f"Exported symbol table to: {symbols_path}")

        return True


def main():
    if len(sys.argv) < 2:
        print("Usage: python assembler.py <file.asm> [K]")
        print("Example: python assembler.py Box.asm 41")
        sys.exit(1)

    asm_file = sys.argv[1]
    k_val = int(sys.argv[2]) if len(sys.argv) >= 3 else 0

    print(f"--- Hack Assembler Initialized (K = {k_val}) ---")
    k_mod_3 = k_val % 3
    print(f"K mod 3 = {k_mod_3}:")
    if k_mod_3 == 0:
        print("  -> Extra Feature: Exporting all labels and variables to symbols.txt")
    elif k_mod_3 == 1:
        print("  -> Extra Feature: Enhanced syntax error reporting with line numbers")
    elif k_mod_3 == 2:
        print("  -> Extra Feature: Warning on duplicate label definitions")

    assembler = HackAssembler(k=k_val)
    success = assembler.assemble(asm_file)
    if success:
        print("Assembly finished successfully.")
    else:
        print("Assembly encountered errors.")


if __name__ == '__main__':
    main()
