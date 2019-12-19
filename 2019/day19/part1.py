from intcode import Computer

STATIONARY = 0
PULLED = 1

def main():
    with open('data.txt', 'r') as f:
        program = f.read().strip().split(',')
    program = [int(d) for d in program]
    affected_count = 0
    for x in range(0, 50):
        for y in range(0, 50):
            computer = Computer(program)
            computer.start()
            computer.set_input(x)
            computer.set_input(y)
            if computer.get_output() == PULLED:
                affected_count += 1
    print(f'{affected_count} points are affected')

if __name__ == '__main__':
    main()
