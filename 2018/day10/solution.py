import copy, math, re, sys

OUTPUT_FILE = 'out.txt'

class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)
        
    def __mul__(self, other):
        return Vector(self.x * other, self.y * other)
        
    def __str__(self):
        return '<{}, {}>'.format(self.x, self.y)

class Light:
    def __init__(self, position, velocity):
        self.position = position
        self.velocity = velocity
        
    def position_at(self, seconds):
        return self.position + self.velocity * seconds
        
    def __str__(self):
        return '{} {}'.format(self.position, self.velocity)
        
class Frame:
    def __init__(self, positions):
        self.positions = positions
        self.min = Vector(math.inf, math.inf)
        self.max = Vector(0, 0)
        for p in positions:
            self.min = self.min_vector(self.min, p)
            self.max = self.max_vector(self.max, p)
        self.size = (self.max.x - self.min.x + 1) * (self.max.y - self.min.y + 1)
        
    def max_vector(self, v1, v2):
        return Vector(max(v1.x, v2.x), max(v1.y, v2.y))
            
    def min_vector(self, v1, v2):
        return Vector(min(v1.x, v2.x), min(v1.y, v2.y))
        
def binary_search_for_frame_size_inflection_point(lights):
    min_seconds = 0
    max_seconds = 10
    frame = generate_frame(lights, min_seconds)
        
    while generate_frame(lights, max_seconds).size < frame.size:
        max_seconds *= max_seconds
        
    while min_seconds < max_seconds:
        seconds = min_seconds + int((max_seconds - min_seconds) / 2)
        frame1 = generate_frame(lights, seconds)
        frame2 = generate_frame(lights, seconds + 1)
        if frame1.size < frame2.size:
            max_seconds = seconds
        else:
            min_seconds = seconds + 1
            
    return min_seconds
    
def generate_frame(lights, seconds):
    positions = []
    for lt in lights:
        positions.append(lt.position_at(seconds))
    return Frame(positions)
        
def read_lights(file):
    lights = []
    for line in file:
        m = re.match('position=<\s*([\-0-9]+),\s+([\-0-9]+)>\svelocity=<\s*([\-0-9]+),\s+([\-0-9]+)>', line)
        lights.append(Light(Vector(int(m.group(1)), int(m.group(2))), Vector(int(m.group(3)), int(m.group(4)))))
    return lights
    
def write_frame_to_file(file, frame):
    light_map = {}
    for p in frame.positions:
        light_map[(p.x, p.y)] = True
    for y in range(frame.min.y, frame.max.y + 1):
        for x in range(frame.min.x, frame.max.x + 1):
            if (x, y) in light_map.keys():
                file.write('#')
            else:
                file.write('.')
        file.write('\n')
            
with open(sys.argv[1], 'r') as file:
    lights = read_lights(file)
    
seconds = binary_search_for_frame_size_inflection_point(lights)
    
with open(OUTPUT_FILE, 'w') as file:
    write_frame_to_file(file, generate_frame(lights, seconds))

print('Message would appear after {} seconds (see {}).'.format(seconds, OUTPUT_FILE))
