import copy, re, sys

NUM_REGISTERS = 4

class Operation:
    def __init__(self, name):
        self.name = name 

    def execute(self, state, instruction):
        state = copy.deepcopy(state)
        state[instruction[3]] = self.op(
                self.operandA(state, instruction[1]),
                self.operandB(state, instruction[2]))
        return state

    def op(self, operandA, operandB):
        assert False

    def operandA(self, state, value):
        assert False

    def operandB(self, state, value):
        assert False

    def __str__(self):
        return self.name

class OperationIR(Operation):
    def operandA(self, state, value):
        return value 

    def operandB(self, state, value):
        return state[value]

class OperationRI(Operation):
    def operandA(self, state, value):
        return state[value]

    def operandB(self, state, value):
        return value 

class OperationRR(Operation):
    def operandA(self, state, value):
        return state[value]

    def operandB(self, state, value):
        return state[value]

class Add(Operation):
    def op(self, operandA, operandB):
        return operandA + operandB

class AddR(Add, OperationRR):
    def __init__(self):
        super().__init__('addr')

class AddI(Add, OperationRI):
    def __init__(self):
        super().__init__('addi')

class Mul(Operation):
    def op(self, operandA, operandB):
        return operandA * operandB

class MulR(Mul, OperationRR):
    def __init__(self):
        super().__init__('mulr')

class MulI(Mul, OperationRI):
    def __init__(self):
        super().__init__('muli')

class Ban(Operation):
    def op(self, operandA, operandB):
        return operandA & operandB

class BanR(Ban, OperationRR):
    def __init__(self):
        super().__init__('banr')

class BanI(Ban, OperationRI):
    def __init__(self):
        super().__init__('bani')

class Bor(Operation):
    def op(self, operandA, operandB):
        return operandA | operandB

class BorR(Bor, OperationRR):
    def __init__(self):
        super().__init__('borr')

class BorI(Bor, OperationRI):
    def __init__(self):
        super().__init__('bori')

class Set(Operation):
    def op(self, operandA, operandB):
        return operandA

class SetR(Set, OperationRR):
    def __init__(self):
        super().__init__('setr')

class SetI(Set, OperationIR):
    def __init__(self):
        super().__init__('seti')

class GT(Operation):
    def op(self, operandA, operandB):
        return 1 if operandA > operandB else 0

class GTIR(GT, OperationIR):
    def __init__(self):
        super().__init__('gtir')

class GTRI(GT, OperationRI):
    def __init__(self):
        super().__init__('gtri')

class GTRR(GT, OperationRR):
    def __init__(self):
        super().__init__('gtrr')

class Eq(Operation):
    def op(self, operandA, operandB):
        return 1 if operandA == operandB else 0

class EqIR(Eq, OperationIR):
    def __init__(self):
        super().__init__('eqir')

class EqRI(Eq, OperationRI):
    def __init__(self):
        super().__init__('eqri')

class EqRR(Eq, OperationRR):
    def __init__(self):
        super().__init__('eqrr')

class Sample:
    OPERATIONS = [
        AddR(), AddI(),
        MulR(), MulI(),
        BanR(), BanI(),
        BorR(), BorI(),
        SetR(), SetI(),
        GTIR(), GTRI(), GTRR(),
        EqIR(), EqRI(), EqRR()]

    def __init__(self, before, instruction, after):
        self.op_code = instruction[0]
        self.before = before
        self.instruction = instruction
        self.after = after
        self.operations = []

    def behaves_like(self):
        if not self.operations:
            for o in self.OPERATIONS:
                state = o.execute(self.before, self.instruction)
                if state == self.after:
                    self.operations.append(o)
        return self.operations

    def __str__(self):
        return str((self.before, self.instruction, self.after))

class Computer:
    def __init__(self, instruction_set, num_registers):
        self.instruction_set = instruction_set
        self.state = [0] * num_registers

    def execute(self, program):
        for instruction in program:
            operation = self.instruction_set[instruction[0]]
            self.state = operation.execute(self.state, instruction)

def determine_instruction_set(samples):
    instruction_set = {}
    for s in samples:
        if s.op_code in instruction_set:
            instruction_set[s.op_code].intersection_update(
                    set(s.behaves_like()))
        else:
            instruction_set[s.op_code] = set(s.behaves_like())

    known_op_codes = [o for o in instruction_set.keys() if 
            len(instruction_set[o]) == 1]
    unknown_op_codes = [o for o in instruction_set.keys() if 
            len(instruction_set[o]) > 1]

    while len(unknown_op_codes) > 0: 
        new_known_op_codes = []
        for u in unknown_op_codes:
            for k in known_op_codes:
                instruction_set[u].difference_update(instruction_set[k])
                if len(instruction_set[u]) == 1:
                    new_known_op_codes.append(u)
        known_op_codes = new_known_op_codes
        unknown_op_codes = [u for u in unknown_op_codes if
                u not in known_op_codes]

    for op_code in instruction_set.keys():
        assert len(instruction_set[op_code]) == 1
        instruction_set[op_code] = list(instruction_set[op_code])[0]
    return instruction_set

def read_samples_and_program(file):
    samples = []
    before = None
    instruction = None
    after = None
    program = []
    state_re = re.compile('(Before|After):\s+\[([0-9,\s]+)\]')
    instruction_re = re.compile('([0-9\s]+)')
    for line in file:
        line = line.strip()
        m = state_re.match(line)
        if m:
            state = list(map(int, m.group(2).split(', ')))
            if m.group(1) == 'Before':
                before = state 
            else:
                after = state 
        else:
            m = instruction_re.match(line)
            if m:
                instruction = tuple(map(int, m.group(1).split(' ')))
        if before and instruction and after:
            samples.append(Sample(before, instruction, after))
            before = None
            instruction = None
            after = None
        elif not before and instruction:
            program.append(instruction)
    return samples, program

if __name__ == '__main__':
    if sys.argv[1] != 'test':
        with open(sys.argv[1], 'r') as file:
            samples, program = read_samples_and_program(file) 

        instruction_set = determine_instruction_set(samples)

        print('The instruction set is:')
        for i in sorted(instruction_set.keys()):
            print(i, instruction_set[i])

        computer = Computer(instruction_set, NUM_REGISTERS)
        computer.execute(program)

        print('\nThe value of register 0 is {}'.format(computer.state[0]))
        
    else:
        assert AddR().execute([1, 2, 3, 4], (0, 1, 2, 3)) == [1, 2, 3, 5]
        assert AddI().execute([1, 2, 3, 4], (0, 1, 2, 3)) == [1, 2, 3, 4]
        assert MulR().execute([1, 2, 3, 4], (0, 1, 2, 3)) == [1, 2, 3, 6]
        assert MulI().execute([1, 2, 3, 4], (0, 1, 2, 3)) == [1, 2, 3, 4]
        assert BanR().execute([1, 5, 3, 4], (0, 1, 2, 3)) == [1, 5, 3, 1]
        assert BanI().execute([1, 5, 3, 4], (0, 1, 2, 3)) == [1, 5, 3, 0]
        assert BorR().execute([1, 5, 3, 4], (0, 1, 2, 3)) == [1, 5, 3, 7]
        assert BorI().execute([1, 5, 3, 4], (0, 1, 1, 3)) == [1, 5, 3, 5]
        assert SetR().execute([1, 5, 3, 4], (0, 2, 2, 3)) == [1, 5, 3, 3]
        assert SetI().execute([1, 5, 3, 4], (0, 1, 1, 3)) == [1, 5, 3, 1]
        assert GTIR().execute([1, 1, 3, 4], (0, 1, 1, 3)) == [1, 1, 3, 0]
        assert GTRI().execute([0, 1, 0, 0], (0, 1, 0, 3)) == [0, 1, 0, 1]
        assert GTRR().execute([4, 1, 0, 5], (0, 0, 3, 3)) == [4, 1, 0, 0]
        assert EqIR().execute([2, 1, 3, 4], (0, 1, 1, 3)) == [2, 1, 3, 1]
        assert EqRI().execute([0, 1, 0, 5], (0, 3, 2, 3)) == [0, 1, 0, 0]
        assert EqRR().execute([4, 1, 0, 5], (0, 0, 3, 3)) == [4, 1, 0, 0]
