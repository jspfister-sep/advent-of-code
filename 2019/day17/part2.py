from intcode import Computer
import enum, itertools

class Item(enum.IntEnum):
    SCAFFOLD = 35
    SPACE = 46
    NEW_LINE = 10
    ROBOT_UP = 94
    ROBOT_DOWN = 118
    ROBOT_LEFT = 60
    ROBOT_RIGHT = 62

    def is_robot(self):
        values = list(self.__class__)
        return self.value in values[values.index(self.ROBOT_UP):]

    def __str__(self):
        return chr(self.value)

class Direction(enum.IntEnum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

    @classmethod
    def from_item(cls, item):
        if item == Item.ROBOT_UP:
            return cls.UP
        elif item == Item.ROBOT_DOWN:
            return cls.DOWN
        elif item == Item.ROBOT_LEFT:
            return cls.LEFT
        elif item == Item.ROBOT_RIGHT:
            return cls.RIGHT
        else:
            assert False

    def opposite(self):
        return self.__class__((self.value + 2) % len(self.__class__))

    def to_left(self):
        new_value = self.value - 1
        if new_value < 0:
            new_value = len(self.__class__) - 1
        return self.__class__(new_value)

    def to_right(self):
        return self.__class__((self.value + 1) % len(self.__class__))

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def adjacent(self, direction):
        x = self.x
        y = self.y
        if direction == Direction.UP:
            y -= 1
        elif direction == Direction.RIGHT:
            x += 1
        elif direction == Direction.DOWN:
            y += 1
        elif direction == Direction.LEFT:
            x -= 1
        else:
            assert False
        return self.__class__(x, y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash(self.x) ^ hash(self.y)

    def __repr__(self):
        return f'({self.x}, {self.y})'

class Path(list):
    def __init__(self, value):
        self.raw_str = ''.join(value)
        self.out_str = ','.join(value)
        super().__init__(value)

    def __str__(self):
        return self.out_str
        
NUM_FUNCTIONS = 3
MAX_FUNCTION_LENGTH = 20

def functions_cover_path(path, functions):
    path_str = path.raw_str
    for f in functions:
        path_str = path_str.replace(f.raw_str, 'X')
    return len([c for c in path_str if c != 'X']) == 0
        
def functions_overlap(path, functions):
    for f1, f2 in itertools.combinations(functions, 2):
        if two_functions_overlap(path, f1, f2):
            return True
    return False

def get_dust_collection_amount(program):
    program[0] = 2 # Wake up robot
    computer = Computer(program)
    computer.start()
    image, robot_position, robot_direction = read_image_output(computer)
    print_image(image) 
    print(f'\nRobot found at {robot_position} facing {str(robot_direction)}')
    path = get_scaffold_path(image, robot_position, robot_direction)
    print(f'Coverage path:\n{path}')
    functions, main_routine = get_functions(path)
    process_computer_output(computer)
    return run_traversal_program(computer, functions, main_routine)

def get_functions(path):
    functions = get_possible_functions(path)
    for f1, f2, f3 in itertools.combinations(functions, NUM_FUNCTIONS):
        function_list = [f1, f2, f3]
        if (not functions_overlap(path, function_list) and
                functions_cover_path(path, function_list)):
            main_routine = get_main_routine(path, function_list)
            if len(main_routine.out_str) <= MAX_FUNCTION_LENGTH:
                return function_list, main_routine
    assert 'No solution found!'

def get_main_routine(path, function_list):
    path_str = path.raw_str
    function_name = 'A'
    for f in function_list:
        path_str = path_str.replace(f.raw_str, function_name)
        function_name = chr(ord(function_name) + 1)
    return Path(list(path_str))

def get_possible_functions(path):
    possible_functions = [] 
    for function_length in range(2, len(path)):
        for start_index in range(len(path) - function_length + 1):
            function = Path(path[start_index:start_index + function_length])
            if (function not in possible_functions and
                    len(function.out_str) <= MAX_FUNCTION_LENGTH and
                    path.raw_str.count(function.raw_str) > 1):
                possible_functions.append(function)
    return possible_functions

def get_scaffold_path(image, robot_position, robot_direction):
    path = []
    move_count = 0
    position = robot_position
    direction = robot_direction
    while True:
        if is_scaffold(image, position.adjacent(direction)):
            move_count += 1
            position = position.adjacent(direction)
        elif is_scaffold(image, position.adjacent(direction.to_left())):
            if move_count > 0:
                path.append(str(move_count))
                move_count = 0
            path.append('L')
            direction = direction.to_left()
        elif is_scaffold(image, position.adjacent(direction.to_right())):
            if move_count > 0:
                path.append(str(move_count))
                move_count = 0
            path.append('R')
            direction = direction.to_right()
        else:
            break
    path.append(str(move_count))
    return Path(path)

def is_intersection(image, x, y):
    return (_is_scaffold(image, x, y) and
            _is_scaffold(image, x, y - 1) and
            _is_scaffold(image, x + 1, y) and
            _is_scaffold(image, x, y + 1) and
            _is_scaffold(image, x - 1, y))

def is_scaffold(image, point):
    if point.y < len(image) and point.x < len(image[0]):
        return image[point.y][point.x] == Item.SCAFFOLD
    return False

def print_image(image):
    for y in range(len(image)):
        for x in range(len(image[0])):
            print(str(image[y][x]), end='')
        print('')

def process_computer_output(computer):
    while computer.has_output():
        output = computer.get_output()
        if output < 256:
            print(chr(output), end='')
        else:
            return output

def read_image_output(computer):
    y = 0
    x = 0
    line = []
    image = []
    last_item = None
    while computer.has_output():
        item = Item(computer.get_output())
        if item == Item.NEW_LINE and last_item == Item.NEW_LINE:
            break
        last_item = item
        if item != Item.NEW_LINE:
            line.append(item)
            if item.is_robot():
                robot_position = Point(x, y)
                robot_direction = Direction.from_item(item)
            x += 1
        elif len(line) > 0:
            image.append(line)
            line =[]
            y += 1
            x = 0
    return image, robot_position, robot_direction

def read_program():
    with open('data.txt', 'r') as f:
        data = f.read().strip().split(',')
    return [int(d) for d in data]

def run_traversal_program(computer, functions, main_routine):
    set_computer_input(computer, main_routine.out_str)
    for f in functions:
        process_computer_output(computer)
        set_computer_input(computer, f.out_str)
    process_computer_output(computer)
    set_computer_input(computer, 'n')
    output = process_computer_output(computer)
    return output

def set_computer_input(computer, string):
    for c in string:
        print(c, end='')
        computer.set_input(ord(c))
    computer.set_input(ord('\n'))
    print('')

def two_functions_overlap(path, f1, f2):
    f2_count = path.raw_str.count(f2.raw_str)
    return path.raw_str.replace(f1.raw_str, 'X').count(f2.raw_str) < f2_count

#####################################################################

def main():
    with open('data.txt', 'r') as f:
        program = read_program()
    dust_amount = get_dust_collection_amount(program)
    print(f'The robot collected {dust_amount} units of dust')

if __name__ == '__main__':
    main()

