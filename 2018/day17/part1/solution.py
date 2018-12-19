import math, re, sys

SPRING_LOCATION = (500, 0)
    
class Map:
    SAND = '.'
    CLAY = '#'
    MOVING_WATER = '|'
    STILL_WATER = '~'
    PENDING_WATER = '?'

    def __init__(self):
        self.data = {}
        self.explored_tiles = {}
        self.minx = math.inf
        self.maxx = 0
        self.miny = math.inf
        self.maxy = 0

    def add_section(self, minx, maxx, miny, maxy):
        if maxx != None and maxy != None:
            for x in range(minx, maxx + 1):
                for y in range(miny, maxy + 1):
                    self.data[(x, y)] = self.CLAY 
        elif maxx == None:
            x = minx
            for y in range(miny, maxy + 1):
                self.data[(x, y)] = self.CLAY 
        else:
            y = miny
            for x in range(minx, maxx + 1 ):
                self.data[(x, y)] = self.CLAY 

    def is_tile(self, x, y, type):
        return self.data.get((x, y), self.SAND) == type

    def load_from_file(self, file):
        clay_re = re.compile('(x|y)=([0-9.]+),\s+(x|y)=([0-9.]+)')
        for line in file:
            m = clay_re.match(line)
            if m.group(1) == 'x':
                x_list = m.group(2).split('.')
                y_list = m.group(4).split('.')
            else:
                y_list = m.group(2).split('.')
                x_list = m.group(4).split('.')
            minx = int(x_list[0])
            maxx = int(x_list[2]) if len(x_list) > 1 else None
            miny = int(y_list[0])
            maxy = int(y_list[2]) if len(y_list) > 1 else None
            self.minx = min(self.minx, minx)
            self.maxx = max(self.maxx, minx, maxx if maxx else 0)
            self.miny = min(self.miny, miny)
            self.maxy = max(self.maxy, miny, maxy if maxy else 0)
            self.add_section(minx, maxx, miny, maxy)

    def mark_until(self, tile_stack, stop, tile_type):
        stop_x, stop_y = stop
        num_water_tiles = 0
        while True:
            x, y = tile_stack.pop()
            self.data[(x, y)] = tile_type
            if ((tile_type == self.STILL_WATER or tile_type == self.MOVING_WATER) and
                    y >= self.miny):
                num_water_tiles += 1
            if x == stop_x and y == stop_y:
                break
        return num_water_tiles

    def water_tile_count(self, start):
        tile_stack = [start]
        turn_stack = []
        num_water_tiles = 0
        while len(tile_stack) > 0:
            x, y = tile_stack.pop()
            
            if y > self.maxy or self.is_tile(x, y, self.MOVING_WATER):
                if len(turn_stack) > 0:
                    if turn_stack[-1].left == self.SAND:
                        turn_stack[-1].left = self.MOVING_WATER
                        tile_stack.append((turn_stack[-1].x + 1, turn_stack[-1].y))
                    else:
                        num_water_tiles += self.mark_until(tile_stack,
                                (turn_stack[-1].x, turn_stack[-1].y), self.MOVING_WATER)
                        tile_stack.append((turn_stack[-1].x, turn_stack[-1].y))
                        turn_stack.pop()
                else:
                    num_water_tiles += self.mark_until(tile_stack,
                            tile_stack[0], self.MOVING_WATER)
            elif self.is_tile(x, y, self.CLAY):
                if turn_stack[-1].left == self.SAND:
                    turn_stack[-1].left = self.CLAY
                    tile_stack.append((turn_stack[-1].x + 1, turn_stack[-1].y))
                else:
                    if turn_stack[-1].left == self.MOVING_WATER:
                        num_water_tiles += self.mark_until(tile_stack,
                                (turn_stack[-1].x, turn_stack[-1].y), self.MOVING_WATER)
                    elif turn_stack[-1].left == self.CLAY:
                        num_water_tiles += self.mark_until(tile_stack,
                                (turn_stack[-1].x, turn_stack[-1].y), self.STILL_WATER)
                    turn_stack.pop()
            elif not self.is_tile(x, y + 1, self.CLAY) and not self.is_tile(x, y + 1, self.STILL_WATER):
                tile_stack.append((x, y))
                tile_stack.append((x, y + 1))
            elif self.is_tile(x + 1, y, self.PENDING_WATER): 
                self.data[(x, y)] = self.PENDING_WATER
                tile_stack.append((x, y))
                tile_stack.append((x - 1, y))
            elif self.is_tile(x - 1, y, self.PENDING_WATER): 
                self.data[(x, y)] = self.PENDING_WATER
                tile_stack.append((x, y))
                tile_stack.append((x + 1, y))
            else:
                self.data[(x, y)] = self.PENDING_WATER
                tile_stack.append((x, y))
                tile_stack.append((x - 1, y))
                turn_stack.append(Turn(x, y))
        
        return num_water_tiles

    def __str__(self):
        ret_str = ''
        for y in range(self.miny, self.maxy + 1):
            for x in range(self.minx, self.maxx + 1):
                ret_str += self.data.get((x, y), self.SAND)
            ret_str += ('\n')
        return ret_str

class Turn:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.left = Map.SAND
        self.right = Map.SAND

map = Map()

with open(sys.argv[1], 'r') as file:
    map.load_from_file(file)

num_water_tiles = map.water_tile_count(SPRING_LOCATION)

with open('out.txt', 'w') as file:
    file.write(str(map))
    
print('\nNumber of water tiles: {}'.format(num_water_tiles))

