import enum

class Direction(enum.IntEnum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

    @classmethod
    def from_item(cls, item):
        if item == Item.ROBOT_UP:
            return cls.UP
        elif item == Item.ROBOT_DOWN:
            return cls.DOWN
        elif item == Item.ROBOT_LEFT:
            return cls.LEFT
        elif item == Item.ROBOT_RIGHT:
            return cls.RIGHT
        else:
            assert False

    def opposite(self):
        return self.__class__((self.value + 2) % len(self.__class__))

    def to_left(self):
        new_value = self.value - 1
        if new_value < 0:
            new_value = len(self.__class__) - 1
        return self.__class__(new_value)

    def to_right(self):
        return self.__class__((self.value + 1) % len(self.__class__))

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def adjacent(self, direction):
        x = self.x
        y = self.y
        if direction == Direction.UP:
            y -= 1
        elif direction == Direction.RIGHT:
            x += 1
        elif direction == Direction.DOWN:
            y += 1
        elif direction == Direction.LEFT:
            x -= 1
        else:
            assert False
        return self.__class__(x, y)

    def mh_distance_to(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash(self.x) ^ hash(self.y)

    def __repr__(self):
        return f'({self.x}, {self.y})'

