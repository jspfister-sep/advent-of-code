import enum, sys

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
    def __init__(self):
        super().__init__(0, 1)

    def execute(self):
        return int(input('Input parameter: '))

class Output(Op):
    def __init__(self):
        super().__init__(1, 0)

    def execute(self, param):
        print(f'Output parameter: {param}')

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

def run_program(data):
    instruction_index = 0
    
    while instruction_index < len(data):
        instruction = data[instruction_index]
        opcode = int(instruction[-2:])
    
        if opcode == HALT:
            break
        else:
            op = OPS[opcode]
            args = []
            for i in range(0, op.num_input_params):
                if i < len(instruction) - 2:
                    parameter_mode = instruction[-3 - i]
                else:
                    parameter_mode = POSITION
                if parameter_mode == POSITION:
                    args.append(int(data[int(data[instruction_index + i + 1])]))
                else:
                    args.append(int(data[instruction_index + i + 1]))
            result = op.execute(*args)
            if op.num_output_params == 1:
                data[int(data[instruction_index + op.num_input_params + 1])] = str(result)
            new_ip_index = op.get_new_instruction_index()
            if new_ip_index.mode == IpMode.RELATIVE:
                instruction_index += new_ip_index.value
            elif new_ip_index.mode == IpMode.ABSOLUTE:
                instruction_index = new_ip_index.value
            else:
                assert False, f'Bad instruction index mode {new_ip_index.mode}'
    else:
        print('Never encountered a terminate instruction')
    
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

OPS = {
    ADD: Add(),
    MULTIPLY: Multiply(),
    INPUT: Input(),
    OUTPUT: Output(),
    JUMP_IF_TRUE: JumpIfTrue(),
    JUMP_IF_FALSE: JumpIfFalse(),
    LESS_THAN: LessThan(),
    EQUALS: Equals(),
}

if len(sys.argv) > 1:
    raw_data = sys.argv[1]
else:
    with open('data.txt', 'r') as f:
        raw_data = f.read().strip()
data = raw_data.split(',')

run_program(data)