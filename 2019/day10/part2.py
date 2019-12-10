import math, sys

TARGET = 200
ASTEROID = '#'
Q_12_TO_3 = 0
Q_3_TO_6 = 1
Q_6_TO_9 = 2
Q_9_TO_12 = 3

SORT_ORDER = {
        Q_12_TO_3 : True,
        Q_3_TO_6 : False,
        Q_6_TO_9 : True,
        Q_9_TO_12 : False
        }

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distance_to(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y)

    def slope_to(self, other):
        dx = abs(self.x - other.x)
        dy = abs(self.y - other.y)
        return dy/dx if dx > 0 else math.inf

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash(self.x) ^ hash(self.y)

    def __repr__(self):
        return f'({self.x}, {self.y})'

with open(sys.argv[1], 'r') as f:
    asteroids = [] 
    y = 0
    while True:
        line = f.readline().strip()
        if not line:
            break
        for x in range(len(line)):
            if line[x] == ASTEROID:
                asteroids.append(Point(x, y))
        y += 1
    laser = Point(int(sys.argv[2]), int(sys.argv[3]))
    asteroids.remove(laser)

quadrants = [{} for i in range(4)]

for a in asteroids:
    dx = laser.x - a.x
    dy = laser.y - a.y
    if dx <= 0 and dy > 0:
        q = Q_12_TO_3
    elif dx < 0 and dy <= 0:
        q = Q_3_TO_6
    elif dx >= 0 and dy < 0:
        q = Q_6_TO_9
    elif dx > 0 and dy >= 0:
        q = Q_9_TO_12
    else:
        assert False, 'You screwed up your quadrant math'

    quadrants[q].setdefault(laser.slope_to(a), []).append(a)

num_destroyed = 0

while any([q for q in quadrants if any(q.values())]):
    for q in range(len(quadrants)):
        for slope in sorted(quadrants[q].keys(), reverse=SORT_ORDER[q]):
            if quadrants[q][slope]:
                target = min(
                        quadrants[q][slope],
                        key=lambda p: laser.distance_to(p)
                        )
                quadrants[q][slope].remove(target)
                num_destroyed += 1

                if num_destroyed == TARGET:
                    print(f'{num_destroyed - 1} targets were destroyed before'
                            f'{target}.\n{target.x} * 100 + {target.y} = '
                            f'{target.x * 100 + target.y}')
                    exit(0)

print('Failure')
exit(1)

