import enum, itertools, sys, time

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

class AdjustRelativeBase(Op):
    def __init__(self):
        super().__init__(1, 0)

    def execute(self, param):
        return param

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distance_to(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y)

    def slope_to(self, other):
        dx = abs(self.x - other.x)
        dy = abs(self.y - other.y)
        return dy/dx if dx > 0 else math.inf

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash(self.x) ^ hash(self.y)

    def __repr__(self):
        return f'({self.x}, {self.y})'

def run_program(ops, data):
    instruction_index = 0
    relative_base = 0
    
    while instruction_index < len(data):
        instruction = data[instruction_index]
        opcode = int(instruction[-2:])
    
        if opcode == HALT:
            break
        else:
            op = ops[opcode]
            args = []
            parameter_modes = []
            for i in range(0, op.num_input_params + op.num_output_params):
                if i < len(instruction) - 2:
                    parameter_modes.insert(0, instruction[-3 - i])
                else:
                    parameter_modes.insert(0, POSITION)
            for i in range(0, op.num_input_params):
                parameter_mode = parameter_modes.pop()
                if parameter_mode == POSITION:
                    memory_address = int(data[instruction_index + i + 1])
                elif parameter_mode == RELATIVE:
                    memory_address = relative_base + int(
                        data[instruction_index + i + 1])
                else:
                    memory_address = instruction_index + i + 1
                if memory_address >= len(data):
                    data.extend([0] * (memory_address - len(data) + 1))
                args.append(int(data[memory_address]))
            result = op.execute(*args)
            if opcode == ADJUST_REL_BASE:
                relative_base += result
            if op.num_output_params == 1:
                assert parameter_modes[0] != IMMEDIATE, 'Bad output param mode'
                if parameter_modes[0] == POSITION:
                    memory_address = int(data[instruction_index + 
                        op.num_input_params + 1])
                elif parameter_modes[0] == RELATIVE:
                    memory_address = relative_base + int(
                        data[instruction_index + op.num_input_params + 1])
                if memory_address >= len(data):
                    data.extend([0] * (memory_address - len(data) + 1))
                data[memory_address] = str(result)
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
ADJUST_REL_BASE = 9
HALT = 99

# Parameter Modes
POSITION = '0'
IMMEDIATE = '1'
RELATIVE = '2'

EMPTY = 0
WALL = 1
BLOCK = 2
PADDLE = 3
BALL = 4
UNKNOWN = 5

OUTPUT_CHARS = {
        EMPTY : ' ',
        WALL : 'W',
        BLOCK : 'B',
        PADDLE : 'P',
        BALL: 'O',
        UNKNOWN: '?',
        }

DELAY = 0.02

def main():
    if len(sys.argv) > 1:
        raw_data = sys.argv[1]
    else:
        with open('data.txt', 'r') as f:
            raw_data = f.read().strip()
    data = raw_data.split(',')
    data[0] = '2' # Put in quarters

    buffer = []
    tiles = {}
    score = 0

    def draw_and_get_input():
        nonlocal score
        nonlocal tiles

        max_x = max(tiles, key=lambda p: p.x).x
        max_y = max(tiles, key=lambda p: p.y).y
        for y in range(0, max_y + 1):
            for x in range(0, max_x + 1):
                print(OUTPUT_CHARS[tiles[Point(x, y)]], end='')
            print('')
        print(f'Your score: {score}')
        time.sleep(DELAY)

        ball_position = None
        paddle_position = None
        for pos, type in tiles.items():
            if type == BALL:
                ball_position = pos
            elif type == PADDLE:
                paddle_position = pos
        if ball_position and paddle_position:
            if paddle_position.x < ball_position.x:
                return 1
            elif paddle_position.x > ball_position.x:
                return -1
        else:
            assert False, 'Unknown paddle or ball position!'
        return 0

    def output(param):
        nonlocal buffer
        nonlocal tiles
        nonlocal score

        buffer.append(int(param))
        if len(buffer) == 3:
            if buffer[0] == -1 and buffer[1] == 0:
                score = buffer[2]
            else:
                tiles[Point(buffer[0], buffer[1])] = buffer[2]
            buffer = []

    ops = {
        ADD: Add(),
        MULTIPLY: Multiply(),
        INPUT: Input(draw_and_get_input),
        OUTPUT: Output(output),
        JUMP_IF_TRUE: JumpIfTrue(),
        JUMP_IF_FALSE: JumpIfFalse(),
        LESS_THAN: LessThan(),
        EQUALS: Equals(),
        ADJUST_REL_BASE: AdjustRelativeBase(),
    }

    run_program(ops, data)

    print(f'Your final score is {score}')

if __name__ == '__main__':
    main()

