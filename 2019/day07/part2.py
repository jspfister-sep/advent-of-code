import enum, itertools, sys

class IpMode(enum.Enum):
    RELATIVE = 0
    ABSOLUTE = 1

class IpIndex:
    def __init__(self, mode, value):
        self.mode = mode
        self.value = value

class Op:
    def __init__(self, num_input_params, num_output_params):
        self.num_input_params = num_input_params
        self.num_output_params = num_output_params
    
    def execute(self):
        assert False, 'Must be implemented in derived class'

    def get_new_instruction_index(self):
        ip_value = self.num_input_params + self.num_output_params + 1
        return IpIndex(IpMode.RELATIVE, ip_value)

class Add(Op):
    def __init__(self):
        super().__init__(2, 1)

    def execute(self, param1, param2):
        return param1 + param2

class Multiply(Op):
    def __init__(self):
        super().__init__(2, 1)

    def execute(self, param1, param2):
        return param1 * param2

class Input(Op):
    def __init__(self, input_func):
        super().__init__(0, 1)
        self.input_func = input_func

    def execute(self):
        return self.input_func()

class Output(Op):
    def __init__(self, output_func):
        super().__init__(1, 0)
        self.output_func = output_func

    def execute(self, param):
        self.output_func(param)

class JumpIfTrue(Op):
    def __init__(self):
        super().__init__(2, 0)

    def execute(self, param1, param2):
        if param1 != 0:
            self.new_ip = IpIndex(IpMode.ABSOLUTE, param2)
        else:
            self.new_ip = super().get_new_instruction_index()
        
    def get_new_instruction_index(self):
        return self.new_ip

class JumpIfFalse(Op):
    def __init__(self):
        super().__init__(2, 0)

    def execute(self, param1, param2):
        if param1 == 0:
            self.new_ip = IpIndex(IpMode.ABSOLUTE, param2)
        else:
            self.new_ip = super().get_new_instruction_index()
        
    def get_new_instruction_index(self):
        return self.new_ip

class LessThan(Op):
    def __init__(self):
        super().__init__(2, 1)

    def execute(self, param1, param2):
        return 1 if param1 < param2 else 0

class Equals(Op):
    def __init__(self):
        super().__init__(2, 1)

    def execute(self, param1, param2):
        return 1 if param1 == param2 else 0

class Computer:
    def __init__(self, ops, data):
        self.ops = ops
        self.data = data
        self.instruction_index = 0
        self.paused = True

    def run(self):
        self.paused = False
        while self.instruction_index < len(self.data):
            instruction = self.data[self.instruction_index]
            opcode = int(instruction[-2:])
        
            if opcode == HALT:
                return True
            else:
                op = self.ops[opcode]
                args = []
                for i in range(0, op.num_input_params):
                    if i < len(instruction) - 2:
                        parameter_mode = instruction[-3 - i]
                    else:
                        parameter_mode = POSITION
                    if parameter_mode == POSITION:
                        mode_index = int(self.data[self.instruction_index + i + 1])
                        args.append(int(self.data[mode_index]))
                    else:
                        args.append(int(self.data[self.instruction_index + i + 1]))
                result = op.execute(*args)
                if op.num_output_params == 1:
                    param_index = self.instruction_index + op.num_input_params + 1
                    output_index = int(self.data[param_index])
                    self.data[output_index] = str(result)
                new_ip_index = op.get_new_instruction_index()
                if new_ip_index.mode == IpMode.RELATIVE:
                    self.instruction_index += new_ip_index.value
                elif new_ip_index.mode == IpMode.ABSOLUTE:
                    self.instruction_index = new_ip_index.value
                else:
                    assert False, f'Bad index mode {new_ip_index.mode}'

            if self.paused:
                return False
        else:
            print('Never encountered a terminate instruction')

    def pause(self):
        self.paused = True
    
# Op Codes
ADD = 1
MULTIPLY = 2
INPUT = 3
OUTPUT = 4
JUMP_IF_TRUE = 5
JUMP_IF_FALSE = 6
LESS_THAN = 7
EQUALS = 8
HALT = 99

# Parameter Modes
POSITION = '0'
IMMEDIATE = '1'

def main():
    if len(sys.argv) > 1:
        raw_data = sys.argv[1]
    else:
        with open('data.txt', 'r') as f:
            raw_data = f.read().strip()
    data = raw_data.split(',')
    
    phases = [5, 6, 7, 8, 9]
    results = {}
    
    for p in itertools.permutations(phases):
        amp_index = 0
        initialized = [False] * len(phases)
        output = 0
        halted = False

        def get_input():
            nonlocal amp_index
            nonlocal initialized
            nonlocal output
            nonlocal phases
            if not initialized[amp_index]:
                initialized[amp_index] = True
                return p[amp_index]
            else:
                return output
    
        def set_output(param):
            nonlocal amp_index
            nonlocal amps
            nonlocal output
            output = param
            amps[amp_index].pause()
    
        ops = {
            ADD: Add(),
            MULTIPLY: Multiply(),
            INPUT: Input(get_input),
            OUTPUT: Output(set_output),
            JUMP_IF_TRUE: JumpIfTrue(),
            JUMP_IF_FALSE: JumpIfFalse(),
            LESS_THAN: LessThan(),
            EQUALS: Equals(),
        }
    
        amps = []
        for i in range(len(phases)):
            amps.append(Computer(ops, data[:]))

        while halted == False:
            if amps[amp_index].run() and amp_index == len(phases) - 1:
                halted = True
            amp_index = (amp_index + 1) % len(amps)

        results[p] = output
    
    max_output = 0
    max_phases = None
    
    for phases, output in results.items():
        if output > max_output:
            max_output = output
            max_phases = phases
    
    print(f'The phases {max_phases} produce the maximum output of {max_output}.')

if __name__ == '__main__':
    main()

