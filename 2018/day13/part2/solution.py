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
        self.deleted = False

    def collision_with(self, other):
        return (not self.deleted and not other.deleted and
                self.x == other.x and self.y == other.y)

    def move(self):
        if not self.deleted:
            if self.direction == UP:
                self.y -= 1
            elif self.direction == DOWN:
                self.y += 1
            elif self.direction == LEFT:
                self.x -= 1
            else:
                self.x += 1

    def turn(self, track):
        if not self.deleted:
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

    def __str__(self):
        return self.direction

class Map:
    def __init__(self):
        self.rows = []
        self.carts = []

    def add_cart(self, x, y, direction):
        self.carts.append(Cart(x, y, direction))

    def add_row(self, row):
        self.rows.append(row)

    def mark_collisions(self):
        carts_to_remove = []
        for c1, c2 in itertools.combinations(self.carts, 2):
            if c1.collision_with(c2):
                c1.deleted = True
                c2.deleted = True

    def iterate_until_last_cart(self):
        while True:
            self.carts = sorted(self.carts)
            for c in self.carts:
                c.move()
                c.turn(self.track(c.x, c.y))
                self.mark_collisions()
            self.carts[:] = [c for c in self.carts if not c.deleted]
            if len(self.carts) == 1:
                return self.carts[0]

    def track(self, x, y):
        return self.rows[y][x]

    def __str__(self):
        str_out = '\n' 
        for y in range(0, len(self.rows)):
            for x in range(0, len(self.rows[y])):
                for c in self.carts:
                    if c.x == x and c.y == y:
                        str_out += str(c)
                        break
                else:
                    str_out += self.track(x, y)
            str_out += '\n'
        return str_out

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

last_cart = map.iterate_until_last_cart()
print('Last cart at {},{}'.format(last_cart.x, last_cart.y))
