import sys

class Level:
    BUG = '#'
    SIZE = 5
    SPACE = '.'
    UNKNOWN = '?'

    def calculate_next_state(self):
        self.next_state = []
        for y in range(self.SIZE):
            row = []
            for x in range(self.SIZE):
                adjacent_count = 0
                adjacent_count += self._get_adjacent_count(x, y, -1, 0)
                adjacent_count += self._get_adjacent_count(x, y, 1, 0)
                adjacent_count += self._get_adjacent_count(x, y, 0, -1)
                adjacent_count += self._get_adjacent_count(x, y, 0, 1)
                if x == self.mid and y == self.mid:
                    row.append(self.UNKNOWN)
                elif self.is_bug(x, y):
                    if adjacent_count == 1:
                        row.append(self.BUG)
                    else:
                        row.append(self.SPACE)
                elif 1 <= adjacent_count <= 2:
                    row.append(self.BUG)
                else:
                    row.append(self.SPACE)
            self.next_state.append(row)

    def has_border_bug(self):
        num_border_bugs = 0
        num_border_bugs += len([c for c in self.state[0] if c == self.BUG])
        if num_border_bugs == 0:
            num_border_bugs += len([c for c in self.state[-1] if c == self.BUG])
        if num_border_bugs == 0:
            num_border_bugs += len([r for r in self.state if r[0] == self.BUG])
        if num_border_bugs == 0:
            num_border_bugs += len([r for r in self.state if r[-1] == self.BUG])
        return num_border_bugs > 0

    def is_bug(self, x, y):
        assert (0 <= x < self.SIZE and 0 <= y < self.SIZE and
                (x != self.mid or y != self.mid))
        return self.state[y][x] == self.BUG

    @property
    def num_bugs(self):
        num_bugs = 0
        for row in self.state:
            num_bugs += row.count(self.BUG)
        return num_bugs

    def update(self):
        self.state = self.next_state

    def _get_adjacent_count(self, x, y, dx, dy):
        assert -1 <= dx <= 1
        assert -1 <= dy <= 1
        assert dx ^ dy
        if x == 0 and dx == -1:
            return (1 if self.prev and
                    self.prev.state[self.mid][self.mid - 1] == self.BUG else 0)
        elif (x + 1) % self.SIZE == 0 and dx == 1:
            return (1 if self.prev and 
                    self.prev.state[self.mid][self.mid + 1] == self.BUG else 0)
        elif y == 0 and dy == -1:
            return (1 if self.prev and 
                    self.prev.state[self.mid - 1][self.mid] == self.BUG else 0)
        elif (y + 1) % self.SIZE == 0 and dy == 1:
            return (1 if self.prev and 
                    self.prev.state[self.mid + 1][self.mid] == self.BUG else 0)
        elif x == self.mid - 1 and y == self.mid and dx == 1:
            return (len([row for row in self.next.state if row[0] == self.BUG])
                if self.next else 0)
        elif x == self.mid + 1 and y == self.mid and dx == -1 and self.next:
            return (len([row for row in self.next.state if row[-1] == self.BUG])
                if self.next else 0)
        elif y == self.mid - 1 and x == self.mid and dy == 1 and self.next:
            return (len([c for c in self.next.state[0] if c == self.BUG])
                if self.next else 0)
        elif y == self.mid + 1 and x == self.mid and dy == -1 and self.next:
            return (len([c for c in self.next.state[-1] if c == self.BUG])
                if self.next else 0)
        else:
            return 1 if self.state[y + dy][x + dx] == self.BUG else 0

    def __init__(self, state=[[SPACE] * SIZE] * SIZE):
        self.state = state
        self.mid = int(self.SIZE / 2)
        self.state[self.mid][self.mid] = self.UNKNOWN
        self.next = None
        self.prev = None

    def __str__(self):
        out_str = ''
        for y in range(self.SIZE):
            for x in range(self.SIZE):
                out_str += self.state[y][x]
            out_str += '\n'
        return out_str

class State:
    def __init__(self, level0):
        self.level0 = level0

    @classmethod
    def from_file(cls, filename):
        state = []
        with open(filename, 'r') as f:
            for line in f:
                line = line.strip()
                state.append(list(line))
        return cls(Level(state))

    def advance(self, minutes):
        for i in range(minutes):
            level = self.level0
            while level.prev:
                level = level.prev
            bottom_level = level
            while level:
                level.calculate_next_state()
                top_level = level
                level = level.next
            if bottom_level.has_border_bug():
                new_bottom_level = Level()
                new_bottom_level.next = bottom_level
                new_bottom_level.calculate_next_state()
                new_bottom_level.update()
                if new_bottom_level.num_bugs > 0:
                    bottom_level.prev = new_bottom_level
            if top_level.has_border_bug():
                new_top_level = Level()
                new_top_level.prev = top_level
                new_top_level.calculate_next_state()
                new_top_level.update()
                if new_top_level.num_bugs > 0:
                    top_level.next = new_top_level
            level = bottom_level
            while level:
                level.update()
                level = level.next

    @property
    def num_bugs(self):
        num_bugs = 0
        level = self.level0
        while level:
            num_bugs += level.num_bugs
            level = level.prev
        level = self.level0
        while level.next:
            num_bugs += level.next.num_bugs
            level = level.next
        return num_bugs

    def __str__(self):
        out_str = ''
        level_index = 0
        level = self.level0
        while level.prev:
            level = level.prev
            level_index -= 1
        while level:
            out_str += f'Depth {level_index}:\n{str(level)}\n'
            level = level.next
            level_index += 1
        return out_str

def main():
    state = State.from_file(sys.argv[1])
    minutes = int(sys.argv[2])
    state.advance(minutes)
    print(f'There are {state.num_bugs} bugs in total after {minutes} minutes')

if __name__ == '__main__':
    main()

