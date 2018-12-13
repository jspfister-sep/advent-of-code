import itertools, re, sys

UP = '^'
DOWN = 'v'
LEFT = '<'
RIGHT = '>'

class Cart:
    DIRECTIONS = [UP, RIGHT, DOWN, LEFT]
    TURNS = [-1, 0, 1]
    SLASH_CURVE = { UP : RIGHT, DOWN : LEFT, LEFT : DOWN, RIGHT : UP }
    BACKSLASH_CURVE = { UP : LEFT, DOWN : RIGHT, LEFT : UP, RIGHT : DOWN }

    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction
        self.turn_index = 0

    def collision_with(self, other):
        return self.x == other.x and self.y == other.y

    def move(self):
        if self.direction == UP:
            self.y -= 1
        elif self.direction == DOWN:
            self.y += 1
        elif self.direction == LEFT:
            self.x -= 1
        else:
            self.x += 1

    def turn(self, track):
        if track == '/':
            self.direction = self.SLASH_CURVE[self.direction]
        elif track == '\\':
            self.direction = self.BACKSLASH_CURVE[self.direction]
        elif track == '+':
            direction_index = self.DIRECTIONS.index(self.direction)  
            turn = self.TURNS[self.turn_index]
            direction_index = (direction_index + turn) % len(self.DIRECTIONS)
            self.direction = self.DIRECTIONS[direction_index]
            self.turn_index = (self.turn_index + 1) % len(self.TURNS)

    def __lt__(self, other):
        return self.y < other.y or (self.y == other.y and self.x < other.x)

class Map:
    def __init__(self):
        self.rows = []
        self.carts = []

    def add_cart(self, x, y, direction):
        self.carts.append(Cart(x, y, direction))

    def add_row(self, row):
        self.rows.append(row)

    def collision(self):
        for c1, c2 in itertools.combinations(self.carts, 2):
            if c1.collision_with(c2):
                return (c1.x, c1.y)
        return None

    def iterate_until_collision(self):
        while True:
            self.carts = sorted(self.carts)
            for c in self.carts:
                c.move()
                collision = self.collision()
                if collision:
                    return collision 
                else:
                    c.turn(self.track(c.x, c.y))

    def track(self, x, y):
        return self.rows[y][x]

def read_map(file):
    cart_symbols = [UP, DOWN, LEFT, RIGHT]
    track_symbols = ['|', '|', '-', '-']
    y = 0
    map = Map()
    for line in file:
        for c in cart_symbols: 
            while c in line:
                map.add_cart(line.index(c), y, c)
                line = line.replace(c, track_symbols[cart_symbols.index(c)]) 
        map.add_row(line)
        y += 1
    return map

with open(sys.argv[1], 'r') as file:
    map = read_map(file)

collision = map.iterate_until_collision()
print('First collision at {},{}'.format(collision[0], collision[1]))
