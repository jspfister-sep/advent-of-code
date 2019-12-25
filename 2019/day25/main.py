from intcode import Computer

def main():
    with open('data.txt', 'r') as f:
        program = f.read()
    program = [int(i) for i in program.strip().split(',')]
    computer = Computer(program)
    computer.start()
    while True:
        while computer.has_output():
            print(chr(computer.get_output()), end='')
        command = input()
        if command == 'exit':
            break
        command = list(command)
        while command:
            computer.set_input(ord(command.pop(0)))
        computer.set_input(ord('\n'))
    computer.terminate()

if __name__ == '__main__':
    main()
