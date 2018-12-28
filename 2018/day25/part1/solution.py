import re, sys

TOLERANCE = 3

class Point:
    def __init__(self, w, x, y, z):
        self.w = w
        self.x = x
        self.y = y
        self.z = z

    def is_close_to(self, other):
        return abs(self.w - other.w) + abs(self.x - other.x) + abs(self.y - other.y) + abs(self.z - other.z) <= TOLERANCE

    def __str__(self):
        return f'({self.w}, {self.x}, {self.y}, {self.z})'

class ConstellationFinder:
    def __init__(self, input_file):
        self.points = set() 
        for line in input_file:
            m = re.match('([-0-9]+),([-0-9]+),([-0-9]+),([-0-9]+)', line)
            assert m
            self.points.add(Point(int(m.group(1)), int(m.group(2)), int(m.group(3)), int(m.group(4))))

    def find_constellations(self):
        constellations = [] 
        while len(self.points) > 0:
            points_to_test = [self.points.pop()]
            group = {points_to_test[0]}
            while len(points_to_test) > 0:
                points_to_add = set() 
                for p in self.points:
                    for t in points_to_test:
                        if p.is_close_to(t):
                            points_to_add.add(p)
                            break
                points_to_test = list(points_to_add)
                group |= points_to_add
                self.points -= points_to_add 
            constellations.append(group)
        return len(constellations)

if __name__ == '__main__':
    with open(sys.argv[1], 'r') as file:
        c = ConstellationFinder(file)

print(f'There are {c.find_constellations()} constellations')
