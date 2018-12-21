import collections, math, sys

NORTH = 'N'
EAST = 'E'
SOUTH = 'S'
WEST = 'W'

class Room:
    def __init__(self, x, y):
        self.x = x 
        self.y = y 
        self.neighbors = { NORTH : None, EAST : None, SOUTH : None, WEST : None }
        self.distance_from_start = math.inf

    @property
    def position(self):
        return (self.x, self.y)

class Map:
    DIRS = [NORTH, EAST, SOUTH, WEST]
    MOVE = { NORTH : (0, 1), EAST : (1, 0), SOUTH : (0, -1), WEST : (-1, 0) }

    START = 'X'
    ROOM = '.'
    V_DOOR = '|'
    H_DOOR = '-'
    WALL = '#'

    def __init__(self):
        self.rooms = {}
        self.min_x = 0 
        self.max_x = 0
        self.min_y = 0 
        self.max_y = 0

    def add_room(self, parent, direction):
        x = parent.x + self.MOVE[direction][0]
        y = parent.y + self.MOVE[direction][1]
        self.min_x = min(self.min_x, x)
        self.max_x = max(self.max_x, x)
        self.min_y = min(self.min_y, y)
        self.max_y = max(self.max_y, y)
        new_room = self.rooms.get((x, y), Room(x, y)) 
        parent.neighbors[direction] = new_room 
        new_room.neighbors[self.DIRS[(self.DIRS.index(direction) + 2) % len(self.DIRS)]] = parent
        self.rooms[new_room.position] = new_room
        return new_room 

    def discover_rooms(self, map_re):
        room_stack = []
        cur_room = Room(0, 0)
        self.rooms[cur_room.position] = cur_room
        for c in map_re:
            if c in self.DIRS:
                cur_room = self.add_room(cur_room, c) 
            elif c == '(':
                room_stack.append(cur_room)
            elif c == '|':
                cur_room = room_stack[-1]
            elif c == ')':
                room_stack.pop()

    def find_room_gte_1000_doors_away(self):
        q = collections.deque()
        start = self.rooms[(0, 0)]
        start.distance_from_start = 0
        q.append(start)
        while len(q) > 0:
            room = q.popleft()
            for n in room.neighbors.values():
                if n and n.distance_from_start > room.distance_from_start + 1:
                    n.distance_from_start = room.distance_from_start + 1
                    q.append(n)
        return len(list(filter(lambda r: r.distance_from_start >= 1000, self.rooms.values())))

    def __str__(self):
        ret_str = self.WALL * ((self.max_x - self.min_x + 1) * 2 + 1) + '\n'
        for y in range(self.max_y, self.min_y - 1, -1):
            ret_str += self.WALL
            for x in range(self.min_x, self.max_x + 1):
                if (x, y) in self.rooms:
                    ret_str += self.START if (x, y) == (0, 0) else self.ROOM
                    ret_str += self.V_DOOR if self.rooms[(x, y)].neighbors[EAST] else self.WALL
                else:
                    ret_str += self.WALL * 2 
            ret_str += '\n' + self.WALL
            for x in range(self.min_x, self.max_x + 1):
                if (x, y) in self.rooms:
                    ret_str += (self.H_DOOR if self.rooms[(x, y)].neighbors[SOUTH] else self.WALL) + self.WALL
                else:
                    ret_str += self.WALL * 2
            ret_str += '\n'
        return ret_str

map = Map()

with open(sys.argv[1], 'r') as file:
    for line in file:
        map_re = line.strip()

map.discover_rooms(map_re)

print('There are {} rooms at least 1000 doors away'.format(map.find_room_gte_1000_doors_away()))

