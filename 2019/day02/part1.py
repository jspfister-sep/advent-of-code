import sys

def add(a, b):
    return a + b

def multiply(a, b):
    return a * b

ADD = 1
INSTRUCTION_SIZE = 4
MULTIPLY = 2
TERMINATE = 99

if len(sys.argv) > 1:
    raw_data = sys.argv[1]
else:
    with open('data.txt', 'r') as f:
        raw_data = f.read().strip()
data = raw_data.split(',')
data = [int(x) for x in data]

# Override data
data[1] = 12
data[2] = 2

opcode_index = 0

while opcode_index < len(data):
    opcode = data[opcode_index]

    if opcode == ADD:
        op = add
    elif opcode == MULTIPLY:
        op = multiply
    else:
        if opcode != TERMINATE:
            print(f'Unknown opcode {opcode} at position {opcode_index}')
        break

    assert opcode_index + 3 < len(data)

    input1 = data[data[opcode_index + 1]]
    input2 = data[data[opcode_index + 2]]
    data[data[opcode_index + 3]] = op(input1, input2)
    opcode_index += INSTRUCTION_SIZE
else:
    print('Never encountered a terminate instruction')

print(data)

