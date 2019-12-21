from intcode import Computer

JUMPSCRIPT = [
        'NOT A T',
        'NOT B J',
        'OR T J',
        'NOT C T',
        'OR T J',
        'AND D J',
        ]

def program_springdroid(intcode_program):
    computer = Computer(intcode_program)
    computer.start()
    process_computer_output(computer)
    for line in JUMPSCRIPT:
        set_computer_input(computer, line)
    set_computer_input(computer, 'WALK')
    return process_computer_output(computer)

def set_computer_input(computer, input_str):
    for c in input_str:
        computer.set_input(ord(c))
        print(c, end='')
    computer.set_input(ord('\n'))
    print('')

def process_computer_output(computer):
    while computer.has_output():
        output = computer.get_output()
        if output < 256:
            print(chr(output), end='')
        else:
            return output

def main():
    with open('data.txt', 'r') as f:
        program = f.read()
    program = [int(i) for i in program.strip().split(',')]
    hull_damage = program_springdroid(program)
    print(f'The amount of hull damage is {hull_damage}')

if __name__ == '__main__':
    main()
