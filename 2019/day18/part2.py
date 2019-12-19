from navigation import Direction, Point
import math, sys

class State:
    def __init__(self, robot_locations, held_keys=set()):
        self.robot_locations = robot_locations
        self.held_keys = held_keys

    def __eq__(self, other):
        return (self.robot_locations == other.robot_locations and 
                sorted(self.held_keys) == sorted(other.held_keys))

    def __repr__(self):
        return f'({self.robot_locations} {self.held_keys})'

    def __hash__(self):
        hash_value = hash(''.join(sorted(list(self.held_keys))))
        for r in self.robot_locations:
            hash_value ^= hash(r)
        return hash_value

class Item(str):
    START = '@'
    WALL = '#'
    EMPTY = '.'

    def is_door(self):
        return 'A' <= self <= 'Z'
    
    def is_key(self):
        return 'a' <= self <= 'z'

    def is_reachable(self, state):
        return (self != self.WALL and 
                (not self.is_door() or self.lower() in state.held_keys))

class Map:
    def __init__(self, data):
        self.robot_starts = []
        self.data = data
        self._parse_data()

    @classmethod
    def from_file(cls, filename):
        data = []
        with open(filename, 'r') as f:
            for line in f:
                data.append(line.strip())
        return cls(data)

    def get_min_key_collection_steps(self):
        start_state = State(self.robot_starts)
        distance, previous = self._dijkstra(
                start_state,
                self._get_possible_next_states,
                )
        final_states = [s for s in previous.keys() if len(s.held_keys) == len(self.keys)]
        return min([distance[s] for s in final_states])

    def _dijkstra(self, start, get_neighbors, param=None):
        open_set = {start}
        previous = {}
        distance = {start: 0}
        visited = set()

        while open_set:
            current = min(open_set, key=lambda p: distance[p])
            open_set.remove(current)
            visited.add(current)
            for n, n_distance in get_neighbors(current, distance[current], param):
                if n not in visited and n_distance < distance.setdefault(n, math.inf):
                    distance[n] = n_distance
                    previous[n] = current
                    open_set.add(n)
        return distance, previous

    def _get_adjacent_points(self, current_point, current_num_steps, current_state):
        neighbors = []
        for d in Direction:
            neighbor_point = current_point.adjacent(d)
            neighbor_item = self._get_item(neighbor_point)
            if neighbor_item.is_reachable(current_state):
                neighbors.append((neighbor_point, current_num_steps + 1))
        return neighbors

    def _get_item(self, point):
        if point.y < len(self.data) and point.x < len(self.data[0]):
            return Item(self.data[point.y][point.x])
        return Item.WALL

    def _get_possible_next_states(self, current_state, current_num_steps, _param):
        if len(current_state.held_keys) == len(self.keys):
            return [] # Found all keys!
        possible_next_states = set()
        keys = set(self.keys.keys())
        unheld_keys = keys - current_state.held_keys
        for i in range(len(current_state.robot_locations)):
            robot_location = current_state.robot_locations[i]
            distance, previous = self._dijkstra(
                    robot_location,
                    self._get_adjacent_points,
                    current_state
                    )
            for k in unheld_keys:
                if self._is_valid_key_choice(k, previous, current_state):
                    key_location = self.keys[k]
                    new_robot_locations = current_state.robot_locations.copy()
                    new_robot_locations[i] = key_location
                    held_keys = current_state.held_keys | {k}
                    num_steps = current_num_steps + distance[key_location]
                    possible_next_states.add((
                        State(new_robot_locations, held_keys),
                        num_steps
                        ))
        return possible_next_states

    def _is_valid_key_choice(self, key, previous, state):
        # First, filter out keys that are unreachable due to locked doors (i.e.
        # infinitely far away). It is also possible that we hit another key 
        # that we hadn't yet picked up on our way to a target key. We want to 
        # filter these out as well since they are effectively duplicates.
        point = self.keys[key]
        if point not in previous:
            return False
        while point:
            point = previous.setdefault(point, None)
            if point:
                item = self._get_item(point)
                if item.is_key() and item not in state.held_keys:
                    return False
        return True

    def _parse_data(self):
        self.keys = {}
        for y in range(len(self.data)):
            for x in range(len(self.data[0])):
                point = Point(x, y)
                item = self._get_item(point)
                if item == Item.START:
                    self.robot_starts.append(point)
                elif item.is_key():
                    self.keys[item] = point

    def __str__(self):
        ret_str = ''
        for y in range(len(self.data)):
            ret_str += self.data[y] + '\n'
        return ret_str

def main():
    import time
    start_time = time.time()
    m = Map.from_file(sys.argv[1])
    min_steps = m.get_min_key_collection_steps()
    print(f'All keys can be collected in a minimum of {min_steps} steps')
    elapsed_time = time.time() - start_time
    print(f'Ran in {time.strftime("%H:%M:%S", time.gmtime(elapsed_time))}')

if __name__ == '__main__':
    main()

