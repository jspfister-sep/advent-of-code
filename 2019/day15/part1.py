from intcode import Computer
import copy, enum, math, threading

class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash(self.x) ^ hash(self.y)

    def __repr__(self):
        return f'({self.x}, {self.y})'

class Direction(enum.IntEnum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

    def opposite(self):
        return Direction((self.value + 2) % len(Direction))

class Location:
    UNKNOWN = 0

    def __init__(self, position, entry_direction=None, is_goal=False):
        self.position = position
        self.entry_direction = entry_direction
        self.is_goal = is_goal
        self.neighbors = [self.UNKNOWN] * len(Direction)
        if entry_direction is not None:
            self.entry_direction = Direction(entry_direction)

    def get_next_unexplored_direction(self):
        if self.UNKNOWN in self.neighbors:
            return Direction(self.neighbors.index(self.UNKNOWN))
        return None

    def set_neighbor(self, neighbor, direction):
        self.neighbors[direction] = neighbor
        if neighbor is not None:
            neighbor.neighbors[direction.opposite()] = self

    def get_backtrack_direction(self):
        if self.entry_direction is not None:
            return self.entry_direction.opposite()
        return None

class Droid:
    class Command(enum.IntEnum):
        MOVE_NORTH = 1
        MOVE_SOUTH = 2
        MOVE_WEST = 3
        MOVE_EAST = 4

        @classmethod
        def from_direction(cls, direction):
            if direction == Direction.NORTH:
                command = cls.MOVE_NORTH
            elif direction == Direction.EAST:
                command = cls.MOVE_EAST
            elif direction == Direction.SOUTH:
                command = cls.MOVE_SOUTH
            elif direction == Direction.WEST:
                command = cls.MOVE_WEST
            return cls(command)
    
    class Status(enum.IntEnum):
        BLOCKED = 0
        MOVED = 1
        GOAL = 2

class Explorer:
    class Vertex:
        def __init__(self, position):
            self.position = position
            self.distance = math.inf
            self.visited = False

    def __init__(self, program):
        self.__command_event = threading.Event()
        self.__status_event = threading.Event()
        computer = Computer(self.__get_next_command, self.__set_status)
        self.compute_thread = threading.Thread(
                target=lambda: computer.run_program(program))

    def find_shortest_path_to_goal(self):
        self.location_map = self._explore()
        vertices = {} 
        for p in self.location_map.keys():
            v = self.Vertex(p)
            if p == self.starting_position:
                v.distance = 0
            vertices[p] = v

        while len(vertices) > 0:
            p_min_dist = min(vertices, key=lambda p: vertices[p].distance)
            u = vertices.pop(p_min_dist)
            l = self.location_map[u.position]
            if l.is_goal:
                return u.distance
            p_neighbors = [n.position for n in l.neighbors if n is not None]
            unvisited_neighbors = [vertices[p] for p in p_neighbors
                    if p in vertices and not vertices[p].visited]
            for v in unvisited_neighbors:
                v.distance = min(v.distance, u.distance + 1)
            u.visited = True
        return math.inf

    def print_map(self):
        x_vals = [p.x for p in self.location_map.keys()]
        y_vals = [p.y for p in self.location_map.keys()]
        x_min = min(x_vals)
        y_min = min(y_vals)
        x_max = max(x_vals)
        y_max = max(y_vals)
        for y in range(y_min - 1, y_max + 2):
            for x in range(x_min - 1, x_max + 2):
                location = self.location_map.get(Position(x, y))
                if x == 0 and y == 0:
                    symbol = 'S'
                elif location:
                    symbol = 'O' if location.is_goal else ' '
                else:
                    symbol = '|'
                print(symbol, end='')
            print('')

    def _explore(self):
        self.starting_position = Position(0, 0)
        starting_location = Location(self.starting_position)
        location_map = {self.starting_position: starting_location}
        path = [starting_location]
        self.compute_thread.start()
        while len(path) > 0:
            cur_loc = path.pop()
            direction, backtrack = self._get_next_direction(cur_loc)
            if direction is None:
                assert cur_loc == starting_location
                break
            droid_status = self._move(direction, backtrack)
            if backtrack:
                continue
            path.append(cur_loc)
            new_loc = None
            if droid_status != Droid.Status.BLOCKED:
                position = self._get_next_position(cur_loc, direction)
                new_loc = location_map.get(position)
                if new_loc is not None:
                    self._move(direction.opposite(), backtrack)
                else:
                    is_goal = droid_status == Droid.Status.GOAL
                    new_loc = Location(position, direction, is_goal)
                    location_map[position] = new_loc
                    path.append(new_loc)
            cur_loc.set_neighbor(new_loc, direction)
        else:
            assert False, 'Never got back to where I started'
        self.__terminate_program()
        return location_map

    def _get_next_direction(self, location):
        backtrack = False
        direction = location.get_next_unexplored_direction()
        if direction is None:
            direction = location.get_backtrack_direction()
            backtrack = True
        return direction, backtrack

    def _get_next_position(self, current_location, direction):
        x = current_location.position.x
        y = current_location.position.y
        if direction == Direction.NORTH:
            y += 1
        elif direction == Direction.EAST:
            x += 1
        elif direction == Direction.SOUTH:
            y -= 1
        elif direction == Direction.WEST:
            x -= 1
        else:
            assert False, f'Bad direction: {direction}'
        return Position(x, y)

    def _move(self, direction, is_backtrack):
        self.__command = Droid.Command.from_direction(direction)
        self.__command_event.set()
        self.__status_event.wait()
        self.__status_event.clear()
        assert self.__status != Droid.Status.BLOCKED or not is_backtrack
        self.__status = Droid.Status(self.__status)
        return self.__status

    def __get_next_command(self):
        self.__command_event.wait()
        self.__command_event.clear()
        return self.__command

    def __set_status(self, droid_status):
        self.__status = droid_status
        self.__status_event.set()

    def __terminate_program(self):
        # The program seems to terminate on a bad movement command
        self.__command = None
        self.__command_event.set()
        self.compute_thread.join()
    
def read_program():
    with open('data.txt', 'r') as f:
        data = f.read().strip().split(',')
    return [int(d) for d in data]

def main():
    explorer = Explorer(read_program())
    num_commands = explorer.find_shortest_path_to_goal()
    print(f'The droid can reach the oxygen system in {num_commands} commands')

if __name__ == '__main__':
    main()
