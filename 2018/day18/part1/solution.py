import sys

class Map:
    OPEN = '.'
    FOREST = '|'
    LUMBERYARD = '#'
    ADJACENT_DIFFS = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]

    def __init__(self):
        self.rows = []

    def adjacent_gte(self, x, y, terrain, count):
        for diff in self.ADJACENT_DIFFS:
            if self.is_x(x + diff[0], y + diff[1], terrain):
                count -= 1
                if count <= 0:
                    return True
        return False

    def is_forest(self, x, y):
        return self.is_x(x, y, self.FOREST)

    def is_lumberyard(self, x, y):
        return self.is_x(x, y, self.LUMBERYARD)

    def is_open(self, x, y):
        return self.is_x(x, y, self.OPEN)

    def is_x(self, x, y, terrain):
        if 0 <= y < len(self.rows) and 0 <= x < len(self.rows[0]):
            return self.rows[y][x] == terrain
        return False

    def load_from_file(self, file):
        for line in file:
            self.rows.append(line.strip())

    def resource_value(self):
        forest_count = 0
        lumberyard_count = 0
        for row in self.rows:
            forest_count += row.count(self.FOREST)
            lumberyard_count += row.count(self.LUMBERYARD)
        return forest_count, lumberyard_count 

    def tick(self, minutes):
        for m in range(0, minutes):
            new_rows = []
            for y in range(0, len(self.rows)):
                row = list(self.rows[y])
                for x in range(0, len(row)):
                    if self.will_become_forest(x, y):
                        row[x] = self.FOREST
                    elif self.will_become_lumberyard(x, y):
                        row[x] = self.LUMBERYARD
                    elif self.will_become_open(x, y):
                        row[x] = self.OPEN
                new_rows.append(''.join(row))
            self.rows = new_rows

    def will_become_forest(self, x, y):
        return self.is_open(x, y) and self.adjacent_gte(x, y, self.FOREST, 3)

    def will_become_lumberyard(self, x, y):
        return self.is_forest(x, y) and self.adjacent_gte(x, y, self.LUMBERYARD, 3)

    def will_become_open(self, x, y):
        return (self.is_lumberyard(x, y) and
            (not self.adjacent_gte(x, y, self.LUMBERYARD, 1) or
             not self.adjacent_gte(x, y, self.FOREST, 1)))

    def __str__(self):
        ret_str = ''
        for row in self.rows: 
            ret_str += row + '\n'
        return ret_str

map = Map()

with open(sys.argv[1], 'r') as file:
    map.load_from_file(file)

map.tick(10)

if len(map.rows[0]) <= 50:
    print(map)
else:
    with open('out.txt', 'w') as file:
        file.write(str(map))

num_forests, num_lumberyards = map.resource_value()
print('\nResource value: {} x {} = {}'.format(num_forests, num_lumberyards, num_forests * num_lumberyards))

