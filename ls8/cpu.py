"""CPU functionality."""

import sys

# opcodes
HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256 # 256 bytes of memory
        self.reg = [0] * 8 # 8 general purpose registers
        self.PC = 0 # Program Counter - index current instruction
        self.IR = 0 # Instruction Register - copy of current instruction
        self.MAR = 0 # Memory Address Register - holds memory address being read/written
        self.MDR = 0 # Memory Data Register - holds value being read/written
        self.FL = 0 # Flag Register - holds flag status

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def ram_read(self, MAR):
        # self.MAR = address
        # self.MDR = self.ram[self.MAR]

        return self.ram[MAR]

    def ram_write(self, MDR, MAR):
        # self.MDR = value
        # self.MAR = address

        self.ram[MAR] = MDR

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.PC,
            #self.fl,
            #self.ie,
            self.ram_read(self.PC),
            self.ram_read(self.PC + 1),
            self.ram_read(self.PC + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        running = True
        
        while running:
            # get current instruction and store copy in IR register
            self.IR = self.ram_read(self.PC)
            # store bytes
            operand_a = self.ram_read(self.PC + 1)
            operand_b = self.ram_read(self.PC + 2)

            if self.IR == HLT: # end loop
                running = False

            elif self.IR == LDI: # set value of reg to an integer
                self.reg[operand_a] = operand_b
                # point PC to next instruction
                self.PC += 3

            elif self.IR == PRN: # print decimal integer in reg
                print(self.reg[operand_a])
                # point PC to next instruction
                self.PC += 2
