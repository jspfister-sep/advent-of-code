import enum, math, re, sys
from keyed_priority_queue import KeyedPriorityQueue

class Terrain(enum.Enum):
    ROCKY = 0
    WET = 1
    NARROW = 2

class Equipment(enum.Enum):
    TORCH = 0
    ROPE = 1
    NEITHER = 2

class Node:
    MOVE_TIME = 1
    EQUIP_TIME = 7

    EQUIPMENT_OPTIONS = {
            Terrain.ROCKY : { Equipment.TORCH, Equipment.ROPE },
            Terrain.WET : { Equipment.ROPE, Equipment.NEITHER },
            Terrain.NARROW : { Equipment.TORCH, Equipment.NEITHER } }

    NEIGHBOR_POSITIONS = [(1, 0), (0, 1), (-1, 0), (0, -1)]

    def __init__(self, map, x, y, equipment=None, distance=math.inf):
        self.x = x
        self.y = y
        self.distance = distance
        self.equipment = equipment
        self.is_target = map.target_x == self.x and map.target_y == self.y
        self.parent = None 
        self.terrain = self.calculate_terrain(map)

    def calculate_terrain(self, map):
        if (self.x, self.y) in map.erosion_level:
            erosion_level = map.erosion_level[(self.x, self.y)]
        else:
            if (self.x == 0 and self.y == 0) or (self.x == map.target_x and self.y == map.target_y):
                geologic_index = 0
            elif self.y == 0:
                geologic_index = self.x * 16807 
            elif self.x == 0:
                geologic_index = self.y * 48271
            else:
                left_position = (self.x - 1, self.y)
                if left_position not in map.erosion_level:
                    Node(map, left_position[0], left_position[1])
                up_position = (self.x, self.y - 1)
                if up_position not in map.erosion_level:
                    Node(map, up_position[0], up_position[1])
                geologic_index = map.erosion_level[left_position] * map.erosion_level[up_position]
            erosion_level = (geologic_index + map.depth) % 20183
            map.erosion_level[(self.x, self.y)] = erosion_level
        return Terrain(erosion_level % 3)

    def neighbors(self, map, q):
        neighbors = []
        for p in self.NEIGHBOR_POSITIONS:
            x = self.x + p[0]
            y = self.y + p[1]
            if x >= 0 and y >= 0:
                node = Node(map, x, y)
                for e in node.permitted_equipment:
                    if ((x, y), e) not in map.visited:
                        n = q.get(((x, y), e), Node(map, x, y, e))
                        neighbors.append(n)
        return neighbors

    @property
    def permitted_equipment(self):
        return self.EQUIPMENT_OPTIONS[self.terrain]
        
    def set_parent_if_better(self, parent):
        if self.equipment == parent.equipment:
            distance = self.MOVE_TIME
        elif self.equipment in parent.permitted_equipment or parent.equipment in self.permitted_equipment:
            distance = self.EQUIP_TIME + self.MOVE_TIME 
        else:
            distance = self.EQUIP_TIME * 2 + self.MOVE_TIME 
        if self.is_target and self.equipment != Equipment.TORCH:
            distance += self.EQUIP_TIME
        if parent.distance + distance < self.distance:
            self.parent = parent
            self.distance = parent.distance + distance
            return True
        return False

    def __str__(self):
        return f'({self.x}, {self.y}) {self.equipment} {self.distance}'

class Map:
    def __init__(self, depth):
        self.depth = depth
        self.erosion_level = {}
        self.visited = {}

    def find_best_time(self, target_x, target_y):
        worst_case_distance = (target_x + target_y) * (Node.MOVE_TIME + Node.EQUIP_TIME)
        self.target_x = target_x
        self.target_y = target_y
        q = KeyedPriorityQueue() 
        q.insert(((0, 0), Equipment.TORCH), Node(map, 0, 0, Equipment.TORCH, 0), 0)
        q.insert(((0, 0), Equipment.ROPE), Node(map, 0, 0, Equipment.ROPE, Node.EQUIP_TIME), Node.EQUIP_TIME)
        while not q.empty():
            node = q.pop()
            self.visited[((node.x, node.y), node.equipment)] = True
            if node.x == target_x and node.y == target_y:
                break
            if (abs(node.x - target_x) + abs(node.y - target_y)) * Node.MOVE_TIME < worst_case_distance:
                worst_case_distance = min(worst_case_distance,
                        (abs(node.x - target_x) + abs(node.y - target_y)) * (Node.MOVE_TIME + Node.EQUIP_TIME))
                for n in node.neighbors(map, q):
                    if n.set_parent_if_better(node):
                        q.insert(((n.x, n.y), n.equipment), n, n.distance)
        move_time = 0
        n = node.parent
        while n:
            move_time += 1
            n = n.parent
        return move_time, node.distance - move_time
                        
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

move_time, equip_time = map.find_best_time(target[0], target[1])

print(f'Movement time: {move_time}\nEquipment changing time: {equip_time}\nTotal time: {move_time + equip_time}')

