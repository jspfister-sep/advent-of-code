import math, sys

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def distance(self, point):
        return abs(self.x - point.x) + abs(self.y - point.y)
        
    def __str__(self):
        return '({}, {})'.format(self.x, self.y)
        
class MajorPoint(Point):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.area = 0

class Map:
    def __init__(self, input_file):
        self.major_points = []
        min_x = math.inf
        min_y = math.inf
        max_x = 0
        max_y = 0

        for line in input_file:
            x = int(line.split(',')[0])
            y = int(line.split(',')[1].strip())
            min_x = min(x, min_x)
            min_y = min(y, min_y)
            max_x = max(x, max_x)
            max_y = max(y, max_y)
            self.major_points.append(MajorPoint(x, y))
        
        self.min = Point(min_x, min_y)
        self.max = Point(max_x, max_y)

    def assign_to_closest_major_point(self, point):
        closest_major_point = self.closest_major_point(point)
        if closest_major_point:
            if self.is_on_border(point):
                closest_major_point.area = math.inf
            else:
                closest_major_point.area += 1
                
    def closest_major_point(self, point):
        distance_by_major_point = []
        for mp in self.major_points:
            distance_by_major_point.append(mp.distance(point))
        min_distance = min(distance_by_major_point)
        if distance_by_major_point.count(min_distance) == 1:
            return self.major_points[distance_by_major_point.index(min_distance)]
        else:
            return None
        
    def for_each_point(self, action):
        for x in range(self.min.x, self.max.x + 1):
            for y in range(self.min.y, self.max.y + 1):
                action(Point(x, y))
                
    def is_on_border(self, point):
        return (point.x <= self.min.x or point.x >= self.max.x or
                point.y <= self.min.y or point.y >= self.max.y)
                
    def solve(self):
        self.for_each_point(self.assign_to_closest_major_point)
        return max(self.major_points, key=lambda p: p.area if p.area < math.inf else 0)

with open(sys.argv[1], 'r') as file:
    solution_point = Map(file).solve()
                    
print('The size of the largest finite area is {}.'.format(solution_point.area))
print('It is owned by the point {}.'.format(solution_point))
            