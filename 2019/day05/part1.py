import sys

class Op:
    def __init__(self, num_input_params, num_output_params):
        self.num_input_params = num_input_params
        self.num_output_params = num_output_params
    
    def execute(self):
        assert False, 'Must be implemented in derived class'

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
            instruction_index += op.num_input_params + op.num_output_params + 1
    else:
        print('Never encountered a terminate instruction')
    
# Op Codes
ADD = 1
MULTIPLY = 2
INPUT = 3
OUTPUT = 4
HALT = 99

# Parameter Modes
POSITION = '0'
IMMEDIATE = '1'

OPS = {
    ADD: Add(),
    MULTIPLY: Multiply(),
    INPUT: Input(),
    OUTPUT: Output(),
}

if len(sys.argv) > 1:
    raw_data = sys.argv[1]
else:
    with open('data.txt', 'r') as f:
        raw_data = f.read().strip()
data = raw_data.split(',')

run_program(data)