import re, sys

class Op:
    def __init__(self, op):
        self.op = op

    def execute(self, state, rA, rB, rC):
        rA, rB = self.get_operands(state, rA, rB)
        state[rC] = self.op(rA, rB)

class OpIR(Op):
    def get_operands(self, state, rA, rB):
        return rA, state[rB]

class OpRI(Op):
    def get_operands(self, state, rA, rB):
        return state[rA], rB 
        
class OpRR(Op):
    def get_operands(self, state, rA, rB):
        return state[rA], state[rB]
        
class OpIX(Op):
    def get_operands(self, state, rA, rB):
        return rA, None

class OpRX(Op):
    def get_operands(self, state, rA, rB):
        return state[rA], None

class Computer:
    NUM_REGISTERS = 6

    OPS = { 'addr' : OpRR(lambda a, b: a + b),
            'addi' : OpRI(lambda a, b: a + b),
            'mulr' : OpRR(lambda a, b: a * b),
            'muli' : OpRI(lambda a, b: a * b),
            'banr' : OpRR(lambda a, b: a & b),
            'bani' : OpRI(lambda a, b: a & b),
            'borr' : OpRR(lambda a, b: a | b),
            'bori' : OpRI(lambda a, b: a | b),
            'setr' : OpRX(lambda a, b: a),
            'seti' : OpIX(lambda a, b: a),
            'gtir' : OpIR(lambda a, b: 1 if a > b else 0),
            'gtri' : OpRI(lambda a, b: 1 if a > b else 0),
            'gtrr' : OpRR(lambda a, b: 1 if a > b else 0),
            'eqir' : OpIR(lambda a, b: 1 if a == b else 0),
            'eqri' : OpRI(lambda a, b: 1 if a == b else 0),
            'eqrr' : OpRR(lambda a, b: 1 if a == b else 0)}

    def __init__(self):
        self.state = [0] * self.NUM_REGISTERS

    def execute(self, opcode, rA, rB, rC):
        self.state[self.ip_register] = self.ip
        self.OPS[opcode].execute(self.state, rA, rB, rC)
        self.ip = self.state[self.ip_register]
        self.ip += 1

    def load_program(self, file):
        self.program = []
        ip_bind_re = re.compile('#ip\s+(\d)')
        instruction_re = re.compile('([a-z]{4})\s+(\d+)\s+(\d+)\s+(\d+)')
        for line in file:
            line = line.strip()
            m = instruction_re.match(line)
            if m:
                self.program.append((m.group(1), int(m.group(2)),
                                    int(m.group(3)), int(m.group(4))))
            else:
                m = ip_bind_re.match(line)
                self.ip_register = int(m.group(1))
                continue

    def run_program(self):
        self.ip = 0
        while self.ip < len(self.program):
            instruction = self.program[self.ip]
            self.execute(instruction[0], instruction[1], instruction[2], instruction[3])

computer = Computer()

with open(sys.argv[1], 'r') as file:
    computer.load_program(file)

computer.run_program()

print('The value of register 0 is {}'.format(computer.state[0]))

