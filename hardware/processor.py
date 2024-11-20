from hardware.logic_gates import *
from hardware.arithmetic_logic_unit import *
from hardware.memory import *
from hardware.util import *

# takes in four bits and a 16-digit bit
# a, d, and *a are flags to write to the register
# X is input
# cl is clock cycle
# returns three 16-digit bits
class CombinedMemory:
    def __init__(self):
        self.regA = Register()
        self.regD = Register()
        self.ram = RAM_MAX()

    def process(self, a, d, star_a, x, cl):
        res = {}
        res['A'] = self.regA.process(a, x, cl)
        res['D'] = self.regD.process(d, x, cl)
        res['*A'] = self.ram.process(res['A'], star_a, x, cl)

        return res

# takes in four 16-digit bits
# I is the instruction bits
# A, D, and *A are the 16-digit registers
# returns a 16-digit bit and four bits
# R is the result of the ALU operation
class ALUInstruction:
    def process(self, I, A, D, star_A):
        a = select_16(I['12'], star_A, A)

        alu_res = ALU(I['10'], I['9'], I['8'], I['7'], I['6'], D, a)
        cond_res = condition(I['2'], I['1'], I['0'], alu_res)

        res = {}
        res['R'] = alu_res
        res['a'] = I['5']
        res['d'] = I['4']
        res['*a'] = I['3']
        res['j'] = cond_res
        return res

# takes in four 16-digit bits
# returns a 16-digit bit and four bits
class ControlUnit:
    def __init__(self):
        self.alu = ALUInstruction()
    
    def process(self, I, A, D, star_A):
        res_alu = self.alu.process(I, A, D, star_A)

        res = {}
        res['R'] = select_16(I['15'], res_alu['R'], I)
        res['a'] = select_16_to_1(I['15'], res_alu['a'], inv(zero))
        res['d'] = select(I['15'], res_alu['d'], zero)
        res['*a'] = select(I['15'], res_alu['*a'], zero)
        res['j'] = select(I['15'], res_alu['j'], zero)

        return res

# takes in nothing, runs on clock cycle
# returns the result of the instruction
class Computer:
    def __init__(self):
        self.control_unit = ControlUnit()
        self.rom = RAM_MAX()
        self.memory = CombinedMemory()
        self.counter = Counter()
        self.instruction_counter = Counter()
        self.A = zero_16
        self.D = zero_16
        self.star_A = zero_16
        self.j = 0
        self.cl = 0
    
    def cycle_clock(self):
        if self.cl == 0:
            self.cl = 1
        else:
            self.cl = 0
    
    def add_instruction(self, I):
        # run this twice to cycle the clock up and down
        ad = 0
        for x in range(2):
            ad = self.instruction_counter.process(0, zero_16, self.cl)
            self.rom.process(ad, 1, I, self.cl)

            self.cycle_clock()
    
    def cycle(self):
        self.process() # prepare instruction
        self.cycle_clock()

        self.process() # execute instruction
        self.cycle_clock()

        res = self.retrieve_state()
        
        return res
    
    def retrieve_state(self):
        counter_res = self.counter.process(self.j, self.A, self.cl)
        rom_res = self.rom.process(sub_16(counter_res, one_16), 0, zero_16, self.cl)
        control_res = self.control_unit.process(rom_res, self.A, self.D, self.star_A)
        memory_res = self.memory.process(control_res['a'], control_res['d'], control_res['*a'], control_res['R'], self.cl)

        self.A = memory_res['A']
        self.D = memory_res['D']
        self.star_A = memory_res['*A']
        self.j = control_res['j']

        res = {}
        res['A'] = memory_res['A']
        res['D'] = memory_res['D']
        res['*A'] = memory_res['*A']
        
        return res

    def process(self):
        counter_res = self.counter.process(self.j, self.A, self.cl)
        rom_res = self.rom.process(counter_res, 0, zero_16, self.cl)
        control_res = self.control_unit.process(rom_res, self.A, self.D, self.star_A)
        memory_res = self.memory.process(control_res['a'], control_res['d'], control_res['*a'], control_res['R'], self.cl)

        self.A = memory_res['A']
        self.D = memory_res['D']
        self.star_A = memory_res['*A']
        self.j = control_res['j']

        res = {}
        res['A'] = memory_res['A']
        res['D'] = memory_res['D']
        res['*A'] = memory_res['*A']
        
        return res