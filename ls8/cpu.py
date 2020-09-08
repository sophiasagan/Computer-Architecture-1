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
PUSH = 0b01000101
POP = 0b01000110


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

        self.reg[7] = 0xF4 # Init stack pointer to address 0xF4

        self.branchtable = {} # Init branchtable
        self.branchtable[LDI] = self.handle_LDI
        self.branchtable[PRN] = self.handle_PRN
        self.branchtable[HLT] = self.handle_HLT
        
        self.branchtable[PUSH] = self.handle_PUSH
        self.branchtable[POP] = self.handle_POP


    def load(self):
        """Load a program into memory."""
        # Get file name from command line arguments
        if len(sys.argv) != 2:
            print("Usage: cpu.py filename")
            sys.exit(1)

        # address = 0
        
        try:
            with open(sys.argv[1]) as f:
                for line in f:
                    split_line = line.split("#")
                    argument = split_line[0].strip()
                    if argument == "":
                        continue
                    if argument[0] == '1' or argument[0] == '0':
                        instruction = argument[:8]
                        self.ram[self.MAR] = int(instruction, 2)
                        self.MAR += 1

                    # self.ram[address] = int(instruction, 2)
                    # address += 1

        except FileNotFoundError: 
            print(f"{sys.argv[1]} file not found")
            sys.exit(2)


    # load(sys.argv[1])


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        # elif op == "SUB": etc
        elif op == SUB:
            self.reg[reg_a] -= self.reg[reg_b]
        elif op == MUL:
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == DIV:
            self.reg[reg_a] /= self.reg[reg_b]
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

    def handle_HLT(self):
        sys.exit()

    def handle_LDI(self):
        register = self.ram_read(self.PC + 1)
        value = self.ram_read(self.PC + 2)

        self.reg[register] = value

    def handle_PRN(self):
        register = self.ram_read(self.PC + 1)
        print(self.reg[register])

    def handle_POP(self):
        # Get the value from address pointed to by the Stack Pointer
        value = self.ram_read(self.reg[7])

        # Get the register number to copy into
        register = self.ram_read(self.PC + 1)

        # Copy the value into the register
        self.reg[register] = value

        # Increment the Stack Pointer
        self.reg[7] += 1

    def handle_PUSH(self):
        # Decrement the Stack Pointer
        self.reg[7] -= 1

        # Get the register to retrieve the value from
        register = self.ram_read(self.PC + 1)

        # Get the value from the register
        value = self.reg[register]

        # Copy the value to the address pointed to by the SP
        self.ram_write(self.reg[7], value)

    def run(self):
        """Run the CPU."""
        running = True
        
        while running:
            instruction = self.ram_read(self.PC)
            self.IR = instruction

            num_operands = instruction >> 6

            operand_a = self.ram_read(self.PC + 1)
            operand_b = self.ram_read(self.PC + 2)

            alu_op = (instruction >> 5) & 0b1

            if alu_op:
                self.alu(self.IR, operand_a, operand_b)
            else:
                self.branchtable[self.IR]()

            self.PC += num_operands + 1