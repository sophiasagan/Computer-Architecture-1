"""CPU functionality."""

import sys


### OP-Codes ###
HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
ADD = 0b10100000
SUB = 0b10100001
MUL = 0b10100010
DIV = 0b10100011


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256 # 256 bytes of memory
        self.reg = [0] * 8 # 8 general purpose registers
        self.PC = 0 # Program Counter - index current instructio
        self.IR = None # Instruction Register - copy of current instruction
        self.MAR = 0 # Memory Address Register - holds memory address being read/written
        self.MDR = None # Memory Data Register - holds value being read/written
        self.FL = None # Flag Register - holds flag status

        self.branchtable = {}
        self.branchtable[LDI] = self.LDI
        self.branchtable[PRN] = self.PRN
        self.branchtable[HLT] = self.HLT
        self.branchtable[MUL] = self.MUL


    def LDI(self, *operands):
        self.reg[operands[0]] = operands[1]
        self.PC += 3

    def PRN(self, *operands):
        print(self.reg[operands[0]])
        self.PC += 2

    def HLT(self, *operands):
        self.running = False
        self.PC += 1

    def MUL(self, *operands):
        self.alu("MUL", *operands)
        self.PC += 3

    def load(self):
        """Load a program into memory."""
        address = 0

        with open("ls8\examples\mult.ls8") as program:
            for line in program:
                split_line = line.split("#")
                instruction = split_line[0].strip()
                if instruction != "":
                    self.ram[address] = int(instruction, 2)
                    address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        # elif op == "SUB": etc
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.PC,
            # self.FL,
            # self.ie,
            self.ram_read(self.PC),
            self.ram_read(self.PC + 1),
            self.ram_read(self.PC + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def ram_read(self, MAR):
        return self.ram[MAR]

    def ram_write(self, MAR, MDR):
        self.ram[MAR] = MDR

    def run(self):
        """Run the CPU."""
        running = True
        while running:
            register_instruction = self.ram_read(self.PC)
            operand_a = self.ram_read(self.PC + 1)
            operand_b = self.ram_read(self.PC + 2)
            
            if register_instruction in self.branchtable:
                self.branchtable[register_instruction](operand_a, operand_b)
            else:
                exit(1)
            