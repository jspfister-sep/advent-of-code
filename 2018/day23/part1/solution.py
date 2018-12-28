import re, sys
from operator import attrgetter

class Nanobot:
    def __init__(self, x, y, z, r):
        self.x = x
        self.y = y
        self.z = z
        self.r = r

    def in_range(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y) + abs(self.z - other.z) <= self.r

    def all_in_range(self, others):
        return [n for n in others if self.in_range(n)]

    def __str__(self):
        return f'<{self.x}, {self.y}, {self.z}> {self.r}'

def find_nanobot_with_best_range(nanobots):
    return max(nanobots, key=attrgetter('r'))

def read_nanobots_from_file(file):
    nanobots = []
    regex = re.compile('pos=<([-0-9]+),([-0-9]+),([-0-9]+)>,\s+r=(\d+)')
    for line in file:
        line = line.strip()
        m = regex.match(line)
        if m:
            nanobots.append(Nanobot(int(m.group(1)), int(m.group(2)), int(m.group(3)), int(m.group(4))))
        else:
            assert False
    return nanobots

with open(sys.argv[1], 'r') as file:
    nanobots = read_nanobots_from_file(file)
    
best_nanobot = find_nanobot_with_best_range(nanobots)
print(f'There are {len(best_nanobot.all_in_range(nanobots))} nanobots in range of {best_nanobot}')
