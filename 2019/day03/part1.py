import math, sys

UP = 'U'
DOWN = 'D'
LEFT = 'L'
RIGHT = 'R'

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return f'({self.x}, {self.y})'

    def distance(self):
        return abs(self.x) + abs(self.y)

class Interval:
    def __init__(self, min, max):
        self.min = min
        self.max = max

    def __contains__(self, n):
        return self.min <= n <= self.max

    def __eq__(self, other):
        return self.min == other.min and self.max == other.max
    
    def get_closest_intersection_to_origin(self, other):
        min_val = max(self.min, other.min)
        max_val = min(self.max, other.max)
        if min_val <= max_val:
            return min(abs(min_val), abs(max_val))
        else:
            return None

class Segment:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def is_vertical(self):
        return isinstance(self.x, int)

    def get_closest_intersection_to_origin(self, other):
        if self.is_vertical() == other.is_vertical():
            if self.is_vertical() and self.x == other.x:
                y_intersection = self.y.get_closest_intersection_to_origin(other.y)
                if y_intersection:
                    return Point(self.x, y_intersection)
            elif not self.is_vertical() and self.y == other.y:
                x_intersection = self.x.get_closest_intersection_to_origin(other.x)
                if x_intersection:
                    return Point(x_intersection, self.y)
        elif self.is_vertical() and self.x in other.x and other.y in self.y:
            return Point(self.x, other.y)
        elif not self.is_vertical() and self.y in other.y and other.x in self.x:
            return Point(other.x, self.y)
        return None

class Wire:
    def __init__(self, segments):
        self.segments = segments

    @classmethod
    def from_string(cls, string):
        segments = []
        x = 0
        y = 0
        motions = string.split(',')
        for m in motions:
            direction = m[0]
            distance = int(m[1:])
            if direction == UP:
                segments.append(Segment(x, Interval(y, y + distance)))
                y += distance
            elif direction == DOWN:
                segments.append(Segment(x, Interval(y - distance, y)))
                y -= distance
            elif direction == LEFT:
                segments.append(Segment(Interval(x - distance, x), y))
                x -= distance
            elif direction == RIGHT:
                segments.append(Segment(Interval(x, x + distance), y))
                x += distance
        return cls(segments)

    def get_closest_intersection_to_origin(self, other):
        nearest_intersection = Point(math.inf, math.inf)
        for s1 in self.segments:
            for s2 in other.segments:
                intersection = s1.get_closest_intersection_to_origin(s2)
                if (intersection and 
                        intersection != Point(0, 0) and
                        intersection.distance() < nearest_intersection.distance()):
                    nearest_intersection = intersection
        if nearest_intersection.x == math.inf:
            nearest_intersection = None
        return nearest_intersection

if len(sys.argv) > 1:
    wire1 = Wire.from_string(sys.argv[1].strip())
    wire2 = Wire.from_string(sys.argv[2].strip())
else:
    with open('data.txt', 'r') as f:
        wire1 = Wire.from_string(f.readline().strip())
        wire2 = Wire.from_string(f.readline().strip())

intersection = wire1.get_closest_intersection_to_origin(wire2)

assert intersection, 'No intersection!'

print(f'The nearest intersection, {intersection}, '
        f'is {intersection.distance()} units from the origin')

