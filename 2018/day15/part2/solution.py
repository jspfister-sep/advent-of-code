import collections, copy, math, queue, re, sys
from operator import attrgetter
from keyed_priority_queue import KeyedPriorityQueue

class Node:
    def __init__(self, x, y, distance=math.inf):
        self.x = x
        self.y = y
        self.distance = distance
        self.previous_nodes = []

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __lt__(self, other):
        return self.distance < other.distance

class AttackPath:
    def __init__(self, map, start, end):
        self.map = map
        self.end = end
        self.distance = math.inf
        self.find_shortest_distance(start)

    def find_shortest_distance(self, start):
        q = KeyedPriorityQueue() 
        q.insert((start[0], start[1]), Node(start[0], start[1], 0))
        while not q.empty():
            node = q.pop()
            if node.x == self.end[0] and node.y == self.end[1]:
                self.distance = node.distance
                self.end_node = node
                break
            for p in self.map.adjacent_space_points(node.x, node.y):
                neighbor = q.get((p[0], p[1]), Node(p[0], p[1]))
                if neighbor not in node.previous_nodes:
                    if neighbor.distance == node.distance + 1:
                        neighbor.previous_nodes.append(node)
                    elif node.distance + 1 < neighbor.distance:
                        neighbor.distance = node.distance + 1
                        neighbor.previous_nodes = [node]
                        q.insert((p[0], p[1]), neighbor)

    @property
    def steps(self):
        path = collections.deque([self.end_node])
        while len(path) < self.distance:
            previous_nodes = sorted(path[0].previous_nodes,
                    key=attrgetter('y', 'x'))
            path.appendleft(previous_nodes[0])
        return path
        
    def __lt__(self, other):
        return (self.distance < other.distance or
                (self.distance == other.distance and
                 (self.end[1] < other.end[1] or
                  (self.end[1] == other.end[1] 
                   and self.end[0] < other.end[0]))))

class Combatant:
    ATTACK_POWER = 3
    HIT_POINTS = 200
    
    def __init__(self, x, y, type):
        self.x = x
        self.y = y
        self.type = type
        self.hit_points = self.HIT_POINTS
        self.attack_power = self.ATTACK_POWER

    def attack(self, enemy):
        enemy.hit_points -= self.attack_power 

    def find_attack_points(self, map, enemies):
        attack_points = []
        for e in enemies:
            attack_points += map.adjacent_space_points(e.x, e.y)
        return attack_points

    def find_shortest_attack_path(self, map, enemies):
        attack_points = self.find_attack_points(map, enemies)
        attack_paths = []
        if attack_points:
            for p in attack_points:
                attack_paths.append(AttackPath(map,
                    (self.x, self.y), (p[0], p[1]))) 
            best_path = sorted(attack_paths)[0]
            if best_path.distance < math.inf:
                return best_path.steps
        return None

    def is_alive(self):
        return self.hit_points > 0

    def is_dead(self):
        return not self.is_alive()

    def is_elf(self):
        return self.type == Map.ELF

    def is_goblin(self):
        return self.type == Map.GOBLIN

    def in_range(self, enemy):
        return ((self.x == enemy.x and abs(self.y - enemy.y) <= 1) or
                (self.y == enemy.y and abs(self.x - enemy.x) <= 1))

    def move(self, map, x, y):
        map.move_combatant(self.x, self.y, x, y)
        self.x = x
        self.y = y

    def take_turn(self, map, enemies):
        if self.is_alive():
            if not enemies:
                return False
            if not self.try_to_attack(map, enemies):
                if self.try_to_move_in_range(map, enemies):
                    self.try_to_attack(map, enemies)
        return True
        
    def try_to_attack(self, map, enemies):
        in_range = [e for e in enemies if self.in_range(e)] 
        in_range = sorted(sorted(in_range), key=attrgetter('hit_points'))
        if len(in_range) > 0:
            self.attack(in_range[0])
            return True
        return False

    def try_to_move_in_range(self, map, enemies):
        path = self.find_shortest_attack_path(map, enemies)
        if path:
            self.move(map, path[0].x, path[0].y)
            return True
        return False

    def __lt__(self, other):
        return self.y < other.y or (self.y == other.y and self.x < other.x)

    def __str__(self):
        return self.type

class Map:
    ELF = 'E'
    GOBLIN = 'G'
    WALL = '#'
    SPACE = '.'
    COMBATANTS = [ELF, GOBLIN]
    ADJACENT_POINTS = [(-1, 0), (1, 0), (0, 1), (0, -1)]

    def __init__(self):
        self.rows = []
        self.combatants = {} 

    def add_combatant(self, combatant):
        self.combatants[(combatant.x, combatant.y)] = combatant

    def adjacent_space_points(self, x, y):
        return [(x + p[0], y + p[1]) for p in self.ADJACENT_POINTS
                if self.is_space(x + p[0], y + p[1])]
        
    @property
    def elves(self):
        return [c for c in self.combatants.values()
                if c.is_elf() and c.is_alive()]

    def find_min_elf_attack_power(self):
        min_attack_power = 1
        max_attack_power = 200 
        while min_attack_power < (max_attack_power - 1):
            attack_power = min_attack_power + int((max_attack_power - min_attack_power) / 2)
            self.combatants = copy.deepcopy(self.combatants_backup)
            for c in self.combatants.values():
                if c.is_elf():
                    c.attack_power = attack_power
            num_rounds, hit_points = self.fight()
            if num_rounds >= 0:
                max_attack_power = attack_power
                last_victory = (attack_power, num_rounds, hit_points)
            else:
                min_attack_power = attack_power
        return last_victory 

    def fight(self):
        done = False
        num_rounds = 0
        while not done:
            combatants = sorted(self.combatants.values())
            for c in combatants: 
                if not c.take_turn(map,
                        self.goblins if c.is_elf() else self.elves):
                    done = True
                    break
            if self.remove_dead_combatants():
                return -1, -1 
            num_rounds += 1
            print(num_rounds)
        return num_rounds - 1, self.sum_remaining_hit_points()

    @property
    def goblins(self):
        return [c for c in self.combatants.values()
                if c.is_goblin() and c.is_alive()]

    def is_space(self, x, y):
        object = self.object_at(x, y)
        return object == self.SPACE if object else False

    def load_from_file(self, file):
        y = 0
        for line in file:
            for c in self.COMBATANTS:
                x = 0
                while True:
                    x = line.find(c, x)
                    if x >= 0:
                        self.add_combatant(Combatant(x, y, c))
                        x += 1
                    else:
                        break
            row = re.sub('|'.join(self.COMBATANTS), self.SPACE, line)
            self.rows.append(row.strip())
            y += 1
        self.combatants_backup = copy.deepcopy(self.combatants)

    def move_combatant(self, x, y, new_x, new_y):
        combatant = self.combatants[(x, y)]
        del self.combatants[(x, y)]
        self.combatants[(new_x, new_y)] = combatant

    def object_at(self, x, y):
        if y < len(self.rows) and x < len(self.rows[y]):
            if ((x, y) in self.combatants and
                self.combatants[(x, y)].is_alive()):
                return str(self.combatants[(x, y)])
            else:
                return self.rows[y][x]
        return None

    def remove_dead_combatants(self):
        dead_elf = False
        dead_combatants = [c for c in self.combatants.values()
                if c.is_dead()]
        for dc in dead_combatants: 
            if dc.is_elf():
                dead_elf = True
                break
            del self.combatants[(dc.x, dc.y)]
        return dead_elf

    def sum_remaining_hit_points(self):
        sum = 0
        for c in self.combatants.values():
            sum += c.hit_points
        return sum

    def __str__(self):
        ret_str = ''
        for y in range(len(self.rows)):
            for x in range(len(self.rows[y])):
                ret_str += self.object_at(x, y)
            for c in sorted(self.combatants.values()):
                if c.y == y:
                    ret_str += ' {}({})'.format(c.type, c.hit_points)
            ret_str += '\n'
        return ret_str

map = Map()

with open(sys.argv[1], 'r') as file:
    map.load_from_file(file)

elf_attack_power, num_rounds, hit_points = map.find_min_elf_attack_power()

print(map)
print('Elf attack power: {}'.format(elf_attack_power))
print('Num rounds: {}\nTotal remaining hit points: {}\n{} x {} = {}'.format(
    num_rounds, hit_points, num_rounds, hit_points, num_rounds * hit_points))
