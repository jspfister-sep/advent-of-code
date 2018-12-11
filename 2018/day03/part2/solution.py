import re, sys

class Rectangle:
    def __init__(self, line):    
        points = []
        m = re.match('\#([0-9]+)\s+\@\s+([0-9]+),([0-9]+)\:\s+([0-9]+)x([0-9]+)', line)
        self.id = m.group(1)
        self.x1 = int(m.group(2)) + 1
        self.y1 = int(m.group(3)) + 1
        self.x2 = self.x1 + int(m.group(4)) - 1
        self.y2 = self.y1 + int(m.group(5)) - 1
        
    def is_left_of_or_above(self, rectangle):
        return self.x2 < rectangle.x1 or self.y2 < rectangle.y1
    
    def overlaps(self, rectangle):
        return not (self.is_left_of_or_above(rectangle) or rectangle.is_left_of_or_above(self))

rectangles = []

with open(sys.argv[1], "r") as file:
    for line in file:
        rectangles.append(Rectangle(line))
        
rectangles_with_overlap = {}
        
for i in range(len(rectangles)):
    for j in range(i + 1, len(rectangles)):
        if rectangles[i].overlaps(rectangles[j]):
            rectangles_with_overlap[i] = None
            rectangles_with_overlap[j] = None
    if i not in rectangles_with_overlap:
        print('Claim {} does not overlap any other claim'.format(rectangles[i].id))
        break
else:
    print('All claims overlap at least one other claim')
