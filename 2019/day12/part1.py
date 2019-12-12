import re, sys

class Vector:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def sum(self):
        return self.x + self.y + self.z

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y, self.z + other.z)

    def __abs__(self):
        return Vector(abs(self.x), abs(self.y), abs(self.z))

    def __repr__(self):
        return f'<{self.x}, {self.y}, {self.z}>'

class Moon:
    def __init__(self, x, y, z):
        self.position = Vector(x, y, z)
        self.velocity = Vector(0, 0, 0)

    def calculate_dv(self, other):
        dv_x = self.calculate_dv_coord(self.position.x, other.position.x)
        dv_y = self.calculate_dv_coord(self.position.y, other.position.y)
        dv_z = self.calculate_dv_coord(self.position.z, other.position.z)
        return Vector(dv_x, dv_y, dv_z)

    def calculate_dv_coord(self, c1, c2):
        if c2 > c1:
            return 1
        elif c2 < c1:
            return -1
        else:
            return 0

    @property
    def energy(self):
        return abs(self.position).sum() * abs(self.velocity).sum()

    def __repr__(self):
        return f'pos={self.position} vel={self.velocity} e={self.energy}'

POSITION_RE = re.compile('\<x=([\d-]+),\sy=([\d-]+),\sz=([\d-]+)\>')

moons = []
with open(sys.argv[1], 'r') as f:
    for line in f:
        match = POSITION_RE.match(line.strip())
        assert match, 'No line match!'
        moons.append(Moon(
            int(match.group(1)),
            int(match.group(2)),
            int(match.group(3))))

for step in range(0, int(sys.argv[2])):
    dv = []
    for m1 in moons: 
        dv.append(Vector(0, 0, 0))
        for m2 in moons:
            if m1 != m2:
                dv[-1] += m1.calculate_dv(m2)
    for m in moons:
        m.velocity += dv.pop(0)
        m.position += m.velocity

for m in moons:
    print(m)

print(f'The total energy is {sum([m.energy for m in moons])}')

