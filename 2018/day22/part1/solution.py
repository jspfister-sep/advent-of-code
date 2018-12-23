import re, sys

class Map:
    ROCKY = 0
    WET = 1
    NARROW = 2

    def __init__(self, depth):
        self.depth = depth

    def risk(self, max_x, max_y):
        erosion_level = {}
        risk = 0
        for y in range(0, max_y + 1):
            for x in range(0, max_x + 1):
                if (x == 0 and y == 0) or (x == max_x and y == max_y):
                    geologic_index = 0
                elif y == 0:
                    geologic_index = x * 16807 
                elif x == 0:
                    geologic_index = y * 48271
                else:
                    geologic_index = erosion_level[(x - 1, y)] * erosion_level[(x, y - 1)]
                mod_result = (geologic_index + self.depth) % 20183
                erosion_level[(x, y)] = mod_result
                mod_result %= 3
                if mod_result == 0:
                    risk += self.ROCKY
                elif mod_result == 1:
                    risk += self.WET
                else:
                    risk += self.NARROW
        return risk
        
def read_map_info(file):
    for line in file:
        depth_re = re.compile('depth:\s+(\d+)')
        target_re = re.compile('target:\s+(\d+),(\d+)')
        m = depth_re.match(line)
        if m:
            depth = int(m.group(1))
        else:
            m = target_re.match(line)
            if m:
                target = (int(m.group(1)), int(m.group(2)))
    return target, depth

with open(sys.argv[1], 'r') as file:
    target, depth = read_map_info(file)

map = Map(depth)
risk = map.risk(target[0], target[1])

print(f'The risk in getting to ({target[0]}, {target[1]}) is {risk}')
