from intcode import Computer
import enum

class Item(enum.IntEnum):
    SCAFFOLD = 35
    SPACE = 46
    NEW_LINE = 10
    ROBOT_UP = 94
    ROBOT_DOWN = 118
    ROBOT_LEFT = 60
    ROBOT_RIGHT = 62

    def __str__(self):
        return chr(self.value)
   
def calculate_alignment_sum(program):
    computer = Computer(program)
    computer.start()
    alignment_sum = 0
    image = read_image_input(computer)
    print_image(image)
    for y in range(len(image)):
        for x in range(len(image[0])):
            if is_intersection(image, x, y):
                alignment_sum += x * y
    return alignment_sum

def is_intersection(image, x, y):
    return (is_scaffold(image, x, y) and
            is_scaffold(image, x, y - 1) and
            is_scaffold(image, x + 1, y) and
            is_scaffold(image, x, y + 1) and
            is_scaffold(image, x - 1, y))

def is_scaffold(image, x, y):
    if y < len(image) and x < len(image[0]):
        return image[y][x] == Item.SCAFFOLD
    return False

def print_image(image):
    for y in range(len(image)):
        for x in range(len(image[0])):
            print(str(image[y][x]), end='')
        print('')

def read_image_input(computer):
    line = []
    image = []
    while computer.has_output():
        output = computer.get_output()
        if output != Item.NEW_LINE:
            line.append(Item(output))
        elif len(line) > 0:
            image.append(line)
            line =[]
    return image

def read_program():
    with open('data.txt', 'r') as f:
        data = f.read().strip().split(',')
    return [int(d) for d in data]

def main():
    with open('data.txt', 'r') as f:
        program = read_program()
    alignment_sum = calculate_alignment_sum(program)
    print(f'The alignment sum is {alignment_sum}')

if __name__ == '__main__':
    main()

    
