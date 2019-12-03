import sys

def add(a, b):
    return a + b

def multiply(a, b):
    return a * b

def run_program(data, noun, verb):
    # Override data
    data[1] = noun
    data[2] = verb
    
    opcode_index = 0
    
    while opcode_index < len(data):
        opcode = data[opcode_index]
    
        if opcode == ADD:
            op = add
        elif opcode == MULTIPLY:
            op = multiply
        else:
            assert(opcode == TERMINATE, 
                f'Unknown opcode {opcode} at position {opcode_index}')
            break
    
        assert opcode_index + 3 < len(data), 'Ran out of parameters'
    
        input1 = data[data[opcode_index + 1]]
        input2 = data[data[opcode_index + 2]]
        data[data[opcode_index + 3]] = op(input1, input2)
        opcode_index += INSTRUCTION_SIZE
    else:
        print('Never encountered a terminate instruction')
    
    return data[0]
    
ADD = 1
INSTRUCTION_SIZE = 4
MULTIPLY = 2
TERMINATE = 99
TARGET_RESULT = 19690720

if len(sys.argv) > 1:
    raw_data = sys.argv[1]
else:
    with open('data.txt', 'r') as f:
        raw_data = f.read().strip()
data = raw_data.split(',')
data = [int(x) for x in data]

for noun in range(0, 100):
    for verb in range (0, 100):
        result = run_program(data[:], noun, verb)
        if result == TARGET_RESULT:
            print(f'Noun: {noun} Verb: {verb} Result {TARGET_RESULT}')
            print(f'100 * {noun} + {verb} = {100 * noun + verb}')
else:
    print('Never found the answer')

