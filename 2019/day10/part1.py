import itertools, math, sys

ASTEROID = '#'
Q1 = 0
Q2 = 1
Q3 = 2
Q4 = 3

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash(self.x) ^ hash(self.y)

    def __str__(self):
        return f'({self.x}, {self.y})'

with open(sys.argv[1], 'r') as f:
    asteroids = {} 
    y = 0
    while True:
        line = f.readline().strip()
        if not line:
            break
        for x in range(len(line)):
            if line[x] == ASTEROID:
                asteroids[Point(x, y)] = [[] for i in range(4)]
        y += 1

for a1, a2 in itertools.permutations(asteroids, 2):
    dx = a1.x - a2.x
    dy = a1.y - a2.y
    if dx < 0 and dy >= 0:
        q = Q1
    elif dx >= 0 and dy > 0:
        q = Q2
    elif dx > 0 and dy <= 0:
        q = Q3
    else:
        q = Q4

    slope = dy/dx if abs(dx) > 0 else math.inf
    if slope not in asteroids[a1][q]:
        asteroids[a1][q].append(slope)
    
max_detector = None
max_detected = 0

for asteroid, quadrants in asteroids.items():
    num_detected = sum(len(q) for q in quadrants)
    #print(f'Asteroid {asteroid} can detect {num_detected}')
    if num_detected > max_detected:
        max_detected = num_detected
        max_detector = asteroid

print(f'Asteroid {max_detector} can detect the most asteroids ({max_detected})')

