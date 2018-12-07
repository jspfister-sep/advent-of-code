import enum, math, sys

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
    class SearchMode(enum.Enum):
        UNTIL_TRUE = 0
        UNTIL_FALSE = 1
        
    def __init__(self, input_file):
        self.major_points = []
        min_x = math.inf
        min_y = math.inf
        max_x = 0
        max_y = 0
        total_x = 0
        total_y = 0

        for line in input_file:
            x = int(line.split(',')[0])
            y = int(line.split(',')[1].strip())
            total_x += x
            total_y += y
            min_x = min(x, min_x)
            min_y = min(y, min_y)
            max_x = max(x, max_x)
            max_y = max(y, max_y)
            self.major_points.append(MajorPoint(x, y))
        
        self.min = Point(min_x, min_y)
        self.max = Point(max_x, max_y)
        self.avg = Point(int(total_x / len(self.major_points)),
                         int(total_y / len(self.major_points)))
        
    def is_in_bounds(self, point):
        return self.min.x <= point.x <= self.max.x and self.min.y <= point.y <= self.max.y
        
    def search(self, x_values, y_values, test, mode):
        valid_points = []
        for x in x_values:
            for y in y_values:
                point = Point(x, y)
                if self.is_in_bounds(point) and test(point):
                    if mode == Map.SearchMode.UNTIL_FALSE:
                        valid_points.append(point)
                    else:
                        return [point]
        return valid_points
                                
    def spiral_search(self, test, start=None, mode=SearchMode.UNTIL_TRUE):
        valid_points = []
        r = 0 # spiral radius
        if not start:
            start = self.avg
        
        while (start.x - r >= self.min.x or
               start.x + r <= self.max.x or
               start.y - r >= self.min.y or
               start.y + r <= self.max.y):
            valid_points_in_spiral = self.search(set([start.x - r, start.x + r]),
                                               range(start.y - r, start.y + r + 1),
                                               test,
                                               mode)
            if mode == Map.SearchMode.UNTIL_FALSE or not valid_points_in_spiral:
                valid_points_in_spiral += self.search(range(start.x - r + 1, start.x + r),
                                               set([start.y - r, start.y + r]),
                                               test,
                                               mode)
                
            if valid_points_in_spiral:
                if mode == Map.SearchMode.UNTIL_FALSE:
                    valid_points += valid_points_in_spiral
                else:
                    return valid_points_in_spiral[0]
            elif mode == Map.SearchMode.UNTIL_FALSE:
                return valid_points
                
            r += 1
                
        if mode == Map.SearchMode.UNTIL_TRUE:
            return None
        else:
            return math.inf
        
    def total_distance(self, point):
        total_distance = 0
        for mp in self.major_points:
            total_distance += mp.distance(point)
        return total_distance
        
with open(sys.argv[1], 'r') as file:
    map = Map(file)
    
within_tolerance = lambda p: map.total_distance(p) < int(sys.argv[2])

start = map.spiral_search(within_tolerance)

print('Start point: {}'.format(start))

region_points = map.spiral_search(within_tolerance, start, Map.SearchMode.UNTIL_FALSE)

if region_points != math.inf:
    print('The size of the region is {}'.format(len(region_points)))
else:
    print('The region exceeds the bounding box')