from intcode import Computer
from navigation import Point

STATIONARY = 0
PULLED = 1

MIN_WIDTH = 100
MIN_HEIGHT = 100

class BeamAnalyzer:
    def __init__(self, program):
        self.cache = {}
        self.program = program

    def find_first_100_by_100_square(self):
        y = 0
        x_min = 0
        x_max = None
        while True:
            x_min, x_max = self._find_x_bounds(y, x_min, x_max)
            width = x_max - x_min + 1 
            if (width >= MIN_WIDTH and 
                    self._get_value(Point(x_max, y + MIN_HEIGHT - 1)) == PULLED):
                x = x_max - MIN_WIDTH + 1
                while self._get_value(Point(x, y + MIN_HEIGHT - 1)) == PULLED:
                    x -= 1
                if x < x_max - MIN_WIDTH + 1:
                    x += 1
                    break
            y += 1
        return Point(x, y)

    def _find_x_bounds(self, y, x_min, x_max):
        x = x_min
        while self._get_value(Point(x, y)) != PULLED:
            x += 1
        x_min = x
        if x_max is not None:
            x = x_max
        while self._get_value(Point(x, y)) != PULLED:
            x += 1
        while self._get_value(Point(x, y)) == PULLED:
            x += 1
        x_max = x - 1
        return x_min, x_max

    def _get_value(self, point):
        if point not in self.cache:
            self.cache[point] = self._get_value_from_robot(point)
        return self.cache[point]

    def _get_value_from_robot(self, point):
            computer = Computer(self.program)
            computer.start()
            computer.set_input(point.x)
            computer.set_input(point.y)
            return computer.get_output()

    def _print_cache(self):
        x_min = min([p.x for p in self.cache.keys()])
        x_max = max([p.x for p in self.cache.keys()])
        y_min = min([p.y for p in self.cache.keys()])
        y_max = max([p.y for p in self.cache.keys()])
        for y in range(y_min, y_max + 1):
            for x in range(x_min, x_max + 1):
                print(self.cache.get(Point(x, y), '?'), end='')
            print('')

def main():
    with open('data.txt', 'r') as f:
        program = f.read().strip().split(',')
    program = [int(d) for d in program]
    affected_count = 0
    b = BeamAnalyzer(program)
    start_point = b.find_first_100_by_100_square()
    print(f'The first {MIN_WIDTH} x {MIN_HEIGHT} square starts at {start_point}\n'
            f'{start_point.x} * {10000} + {start_point.y} = '
            f'{start_point.x * 10000 + start_point.y}')

if __name__ == '__main__':
    main()
