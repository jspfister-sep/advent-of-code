import itertools, re, sys
from operator import attrgetter

class Point:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def distance_to(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y) + abs(self.z - other.z)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __hash__(self):
        return hash(self.x) ^ hash(self.y) ^ hash(self.z)

    def __str__(self):
        return f'({self.x}, {self.y}, {self.z})'

class Matrix3x3:
    def __init__(self, a, b, c, d, e, f, g, h, i):
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.e = e
        self.f = f
        self.g = g
        self.h = h
        self.i = i

    def determinant(self):
        return (self.a * (self.e * self.i - self.f * self.h)
               -self.b * (self.d * self.i - self.f * self.g)
               +self.c * (self.d * self.h - self.e * self.g))

class Plane:
    def __init__(self, a, b, c, d):
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        
    def intersection_point(self, p1, p2):
        det = Matrix3x3(self.a, self.b, self.c, p1.a, p1.b, p1.c, p2.a, p2.b, p2.c).determinant()
        if det == 0: 
            return None
        else:
            x = Matrix3x3(self.d, self.b, self.c, p1.d, p1.b, p1.c, p2.d, p2.b, p2.c).determinant() / det
            y = Matrix3x3(self.a, self.d, self.c, p1.a, p1.d, p1.c, p2.a, p2.d, p2.c).determinant() / det
            z = Matrix3x3(self.a, self.b, self.d, p1.a, p1.b, p1.d, p2.a, p2.b, p2.d).determinant() / det
        return Point(x, y, z)

    def __hash__(self):
        return hash(self.a) ^ hash(self.b) ^ hash(self.c) ^ hash(self.d)

    def __str__(self):
        return f'{self.a}x + {self.b}y + {self.c}z = {self.d}'

class Octahedron:
    def __init__(self, center, radius):
        self.center = center 
        self.radius = radius
        self.planes = self.calculate_planes()

    def calculate_planes(self):
        planes = [] 
        for a in [-1, 1]:
            for b in [-1, 1]:
                for c in [-1, 1]:
                    planes.append(Plane(a, b, c, a * self.center.x + b * self.center.y + c * self.center.z + self.radius))
        return planes

    def intersects(self, other):
        return self.center.distance_to(other.center) <= self.radius + other.radius

    def __contains__(self, point):
        return self.center.distance_to(point) <= self.radius

    def __hash__(self):
        return hash(self.center) ^ hash(self.radius)

    def __str__(self):
        return f'{self.center} {self.radius}'

class Nanobot(Octahedron):
    def __init__(self, center, radius):
        super().__init__(center, radius)
        self.neighbors = set()

class Teleporter:
    def __init__(self, input_file):
        self.nanobots = self.read_from_file(input_file)
        
    def bron_kerbosch(self, r, p, x, maximal_cliques):
        if not p and not x:
            maximal_cliques.append(r)
        else:
            u = max(p | x, key=lambda s: len(s.neighbors))
            for v in p - u.neighbors:
                self.bron_kerbosch(r | {v}, p & v.neighbors, x & v.neighbors, maximal_cliques)
                p.remove(v)
                x.add(v)

    def calculate_neighbors(self, nanobots):
        for s1, s2 in itertools.combinations(nanobots, 2):
            if s1.intersects(s2):
                s1.neighbors.add(s2)
                s2.neighbors.add(s1)

    def find_best_point(self):
        points = []
        for nanobots in self.find_biggest_intersection_sets(self.nanobots):
            planes = self.get_bounding_planes(nanobots)
            intersection_points = self.find_intersection_points(nanobots, planes)
            points.append(self.find_closest_point_to_origin(intersection_points))
        best_point = self.find_closest_point_to_origin(points) 
        return best_point, best_point.distance_to(Point(0, 0, 0))

    def find_biggest_intersection_sets(self, nanobots):
        self.calculate_neighbors(nanobots)
        r = set()
        p = nanobots
        x = set()
        maximal_cliques = []
        self.bron_kerbosch(r, p, x, maximal_cliques)
        max_clique_size = len(max(maximal_cliques, key=lambda c: len(c)))
        return [c for c in maximal_cliques if len(c) == max_clique_size]

    def find_closest_point_to_origin(self, points):
        origin = Point(0, 0, 0)
        return min(points, key=lambda p: p.distance_to(origin))

    def find_intersection_points(self, nanobots, planes):
        points = set()
        for p1, p2, p3 in itertools.combinations(planes, 3):
            p = p1.intersection_point(p2, p3)
            if p:
                for n in nanobots:
                    if p not in n:
                        break
                else:
                    points.add(p)
        return points

    def get_bounding_planes(self, nanobots):
        planes_by_side = [[] for i in range(8)] 
        for n in nanobots:
            for i in range(len(n.planes)):
                planes_by_side[i].append(n.planes[i])
        bounding_planes = []
        for s in planes_by_side:
            bounding_planes.append(min(s, key=attrgetter('d')))
        return bounding_planes

    def read_from_file(self, file):
        nanobots = set() 
        regex = re.compile('pos=<([-0-9]+),([-0-9]+),([-0-9]+)>,\s+r=(\d+)')
        for line in file:
            line = line.strip()
            m = regex.match(line)
            if m:
                nanobots.add(Nanobot(Point(int(m.group(1)), int(m.group(2)), int(m.group(3))), int(m.group(4))))
            else:
                assert False
        return nanobots


if __name__ == '__main__':
    with open(sys.argv[1], 'r') as file:
        teleporter = Teleporter(file)
    
    best_point, distance = teleporter.find_best_point()
       
    print(f'The best point, {best_point}, is {distance} units from the origin')
