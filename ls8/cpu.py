"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.flags = 0b00000000
        self.looping = False
        self.file = sys.argv
        self.instruction_set = {
            'HLT': 0b00000001,
            'LDI': 0b10000010,
            'PRN': 0b01000111,
            'MUL': 0b10100010,
        }
        self.stack = []
        self.pointer = 0

    def load(self, program=[]):
        """Load a program into memory."""
        if len(sys.argv) != 2:
            print("Usage example_cpu.py filename")


        program = []
        print(int(10000010), "BIN")

        with open(sys.argv[1]) as file:
            for line in file:
                split_line = line.split('#')[0].strip()
                if split_line == "":
                    continue
                else:
                    program.append(int(split_line, 2))

        address = 0

        # split program
        for instruction in program:
            self.ram[address] = instruction
            address += 1

    def ram_read(self, mar):
        return self.ram[mar]

    def ram_write(self, mar, mdr): # memory address register, memory data register
        self.ram[mar] = mdr

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        # reset registers
        self.looping = True


        while self.looping:
            instruction_register = self.ram_read(self.pc)
            is_alu = instruction_register >> 5 & 0b1
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
            num_operands = instruction_register >> 6

            if is_alu == 1: # if 1, needs to pass through the alu
                pass

            if instruction_register == self.instruction_set['HLT']:
                self.looping = False

            if instruction_register == self.instruction_set['LDI']:
                self.reg[operand_a] = operand_b
                self.pc += 3

            if instruction_register == self.instruction_set['MUL']:
                new_val = self.reg[operand_a] * self.reg[operand_b]
                self.reg[operand_a] = new_val
                self.pc += 3

            if instruction_register == self.instruction_set['PRN']:
                print(self.reg[operand_a])
                self.pc += 2
