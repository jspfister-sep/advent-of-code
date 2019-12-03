import math, sys

UP = 'U'
DOWN = 'D'
LEFT = 'L'
RIGHT = 'R'

class Intersection:
    def __init__(self, x, y, steps=0):
        self.x = x
        self.y = y
        self.steps = steps

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return f'({self.x}, {self.y})'

class Interval:
    def __init__(self, min, max, direction):
        self.min = min
        self.max = max
        self.direction = direction

    def __contains__(self, n):
        return self.min <= n <= self.max

    def __eq__(self, other):
        return self.min == other.min and self.max == other.max

    def is_increasing(self):
        return self.direction == UP or self.direction == RIGHT
    
    def get_intersection_with_minimum_steps(self, other):
        min_val = max(self.min, other.min)
        max_val = min(self.max, other.max)
        if min_val <= max_val:
            steps_to_min_val = self.get_steps_to_point(min_val) + other.get_steps_to_point(min_val)
            steps_to_max_val = self.get_steps_to_point(max_val) + other.get_steps_to_point(max_val)
            if steps_to_min_val < steps_to_max_val:
                return (min_val, steps_to_min_val)
            else:
                return (max_val, steps_to_max_val)
        else:
            return None

    def get_steps_to_point(self, n):
        if self.is_increasing():
            return n - self.min
        else:
            return self.max - n

class Segment:
    def __init__(self, x, y, num_prev_steps):
        self.x = x
        self.y = y
        self.num_prev_steps = num_prev_steps

    def is_vertical(self):
        return isinstance(self.x, int)

    def get_intersection_with_minimum_steps(self, other):
        if self.is_vertical() == other.is_vertical():
            if self.is_vertical() and self.x == other.x:
                y_intersection = self.y.get_intersection_with_minimum_steps(other.y)
                if y_intersection:
                    return Intersection(self.x, y_intersection[0], self.num_prev_steps + other.num_prev_steps + y_intersection[1])
            elif not self.is_vertical() and self.y == other.y:
                x_intersection = self.x.get_intersection_with_minimum_steps(other.x)
                if x_intersection:
                    return Intersection(x_intersection[0], self.y, self.num_prev_steps + other.num_prev_steps + x_intersection[1])
        elif self.is_vertical() and self.x in other.x and other.y in self.y:
            return Intersection(self.x, other.y,
                    self.num_prev_steps + other.num_prev_steps +
                    self.y.get_steps_to_point(other.y) + other.x.get_steps_to_point(self.x))
        elif not self.is_vertical() and self.y in other.y and other.x in self.x:
            return Intersection(other.x, self.y,
                    self.num_prev_steps + other.num_prev_steps +
                    self.x.get_steps_to_point(other.x) + other.y.get_steps_to_point(self.y))
        return None

class Wire:
    def __init__(self, segments):
        self.segments = segments

    @classmethod
    def from_string(cls, string):
        segments = []
        x = 0
        y = 0
        steps = 0
        motions = string.split(',')
        for m in motions:
            direction = m[0]
            distance = int(m[1:])
            if direction == UP:
                segments.append(Segment(x, Interval(y, y + distance, direction), steps))
                y += distance
            elif direction == DOWN:
                segments.append(Segment(x, Interval(y - distance, y, direction), steps))
                y -= distance
            elif direction == LEFT:
                segments.append(Segment(Interval(x - distance, x, direction), y, steps))
                x -= distance
            elif direction == RIGHT:
                segments.append(Segment(Interval(x, x + distance, direction), y, steps))
                x += distance
            steps += distance
        return cls(segments)

    def get_intersection_with_minimum_steps(self, other):
        first_intersection = Intersection(0, 0, math.inf)
        for s1 in self.segments:
            for s2 in other.segments:
                intersection = s1.get_intersection_with_minimum_steps(s2)
                if (intersection and 
                        intersection != Intersection(0, 0) and
                        intersection.steps < first_intersection.steps):
                    first_intersection = intersection
        if first_intersection.steps == math.inf:
            first_intersection = None
        return first_intersection

if len(sys.argv) > 1:
    wire1 = Wire.from_string(sys.argv[1].strip())
    wire2 = Wire.from_string(sys.argv[2].strip())
else:
    with open('data.txt', 'r') as f:
        wire1 = Wire.from_string(f.readline().strip())
        wire2 = Wire.from_string(f.readline().strip())

intersection = wire1.get_intersection_with_minimum_steps(wire2)

assert intersection, 'No intersection!'

print(f'The nearest intersection, {intersection}, '
        f'is {intersection.steps} total steps from the origin')

