from navigation import Direction, Point
import math, sys

class State:
    def __init__(self, point, level=0):
        self.point = point
        self.level = level

    def __eq__(self, other):
        return self.point == other.point and self.level == other.level

    def __repr__(self):
        return f'({self.point}, {self.level})'

    def __hash__(self):
        return hash(self.point) ^ hash(self.level)

class Item(str):
    WALL = '#'
    NAVIGABLE = '.'
    START = 'A'
    END = 'Z'

    def is_capital(self):
        return 'A' <= self <= 'Z'

class Map:
    def __init__(self, data):
        self.data = data
        self._parse_data()

    @classmethod
    def from_file(cls, filename):
        data = []
        with open(filename, 'r') as f:
            for line in f:
                data.append(line.strip('\n'))
        return cls(data)

    def get_min_steps(self):
        self._compute_neighbor_lookup_table()
        distance = self._a_star(self.start, self._get_adjacent_states)
        return distance[self.end]

    def _a_star(self, start, get_neighbors):
        open_set = {start}
        gscore = {start: 0}
        fscore = {start: 0}

        while open_set:
            current = min(open_set, key=lambda s: fscore[s])
            if current == self.end:
                break
            open_set.remove(current)
            for n, n_gscore in get_neighbors(current, gscore[current]):
                if n_gscore < gscore.setdefault(n, math.inf):
                    gscore[n] = n_gscore
                    fscore[n] = n_gscore + self._estimate_distance_to_goal(n)
                    open_set.add(n)
        return gscore

    def _compute_neighbor_lookup_table(self):
        self.neighbor_lookup_table = {}
        portals = set(self.inner_portals.keys()) | set(self.outer_portals.keys())
        source_set = {self.start.point} | portals
        destination_set = portals | {self.end.point}
        while source_set:
            source = source_set.pop()
            self.neighbor_lookup_table[source] = set()
            distance = self._dijkstra(source, self._get_adjacent_points)
            for destination in destination_set - {source}:
                num_steps = distance.get(destination, math.inf)
                if num_steps < math.inf:
                    self.neighbor_lookup_table[source].add((destination, num_steps))

    def _dijkstra(self, start, get_neighbors):
        open_set = {start}
        distance = {start: 0}
        visited = set()

        while open_set:
            current = min(open_set, key=lambda p: distance[p])
            open_set.remove(current)
            visited.add(current)
            for n, n_distance in get_neighbors(current, distance[current]):
                if n not in visited and n_distance < distance.setdefault(n, math.inf):
                    distance[n] = n_distance
                    open_set.add(n)
        return distance

    def _estimate_distance_to_goal(self, state):
        if self.end.level == state.level:
            return state.point.mh_distance_to(self.end.point)
        return state.level * 2

    def _find_access_point(self, point, adjacent_point):
        access_point = None
        if point.x == adjacent_point.x:
            candidate_point = Point(point.x, min(point.y, adjacent_point.y) - 1)
            if self._get_item(candidate_point) == Item.NAVIGABLE:
                access_point = candidate_point
            else:
                candidate_point = Point(point.x, max(point.y, adjacent_point.y) + 1)
                if self._get_item(candidate_point) == Item.NAVIGABLE:
                    access_point = candidate_point
        elif point.y == adjacent_point.y:
            candidate_point = Point(min(point.x, adjacent_point.x) - 1, point.y)
            if self._get_item(candidate_point) == Item.NAVIGABLE:
                access_point = candidate_point
            else:
                candidate_point = Point(max(point.x, adjacent_point.x) + 1, point.y)
                if self._get_item(candidate_point) == Item.NAVIGABLE:
                    access_point = candidate_point
        return access_point

    def _get_adjacent_points(self, current_point, current_num_steps):
        neighbors = set()
        for d in Direction:
            neighbor_point = current_point.adjacent(d)
            neighbor_item = self._get_item(neighbor_point)
            if neighbor_item == Item.NAVIGABLE:
                neighbors.add((neighbor_point, current_num_steps + 1))
        return neighbors

    def _get_adjacent_states(self, current_state, current_num_steps):
        neighbors = set()
        for neighbor in self.neighbor_lookup_table[current_state.point]:
            neighbor_point = neighbor[0]
            neighbor_distance = current_num_steps + neighbor[1]
            if neighbor_point == self.end.point:
                if current_state.level > self.end.level:
                    continue
                neighbor_level = current_state.level
            elif neighbor_point in self.inner_portals:
                neighbor_point = self.inner_portals[neighbor_point]
                neighbor_distance += 1
                neighbor_level = current_state.level + 1
            elif neighbor_point in self.outer_portals:
                if current_state.level == self.end.level:
                    continue
                neighbor_point = self.outer_portals[neighbor_point]
                neighbor_distance += 1
                neighbor_level = current_state.level - 1
            else:
                assert False, f'Why is {neighbor} in the lookup table?!'
            neighbors.add((State(neighbor_point, neighbor_level), neighbor_distance))
        return neighbors

    def _get_item(self, point):
        if point.y < len(self.data) and point.x < len(self.data[0]):
            return Item(self.data[point.y][point.x])
        return Item(Item.WALL)

    def _parse_data(self):
        self.inner_portals = {}
        self.outer_portals = {}
        incomplete_portals = {}
        min_x = 2
        max_x = len(self.data[0]) - 3
        min_y = 2
        max_y = len(self.data) - 3
        for y in range(len(self.data)):
            for x in range(len(self.data[0])):
                point = Point(x, y)
                item = self._get_item(point)
                if item.is_capital():
                    for d in Direction:
                        adjacent_point = point.adjacent(d)
                        adjacent_item = self._get_item(adjacent_point)
                        if adjacent_item.is_capital():
                            access_point = self._find_access_point(point, adjacent_point)
                            if access_point:
                                if item == adjacent_item == Item.START:
                                    self.start = State(access_point)
                                elif item == adjacent_item == Item.END:
                                    self.end = State(access_point)
                                else:
                                    portal_characters = sorted([item, adjacent_item])
                                    portal_name = ''.join(portal_characters)
                                    first_portal_point = incomplete_portals.setdefault(
                                            portal_name,
                                            access_point
                                            )
                                    if first_portal_point != access_point:
                                        if (access_point.x == min_x or 
                                                access_point.x == max_x or 
                                                access_point.y == min_y or
                                                access_point.y == max_y):
                                            self.outer_portals[access_point] =\
                                                    first_portal_point
                                            self.inner_portals[first_portal_point] =\
                                                    access_point
                                        else:
                                            self.inner_portals[access_point] =\
                                                    first_portal_point
                                            self.outer_portals[first_portal_point] =\
                                                    access_point

    def __str__(self):
        ret_str = ''
        for y in range(len(self.data)):
            ret_str += self.data[y] + '\n'
        return ret_str

def main():
    import time
    start_time = time.time()
    m = Map.from_file(sys.argv[1])
    min_steps = m.get_min_steps()
    print(f'The maze can be nagivated in a minimum of {min_steps} steps')
    elapsed_time = time.time() - start_time
    print(f'Ran in {time.strftime("%H:%M:%S", time.gmtime(elapsed_time))}')

if __name__ == '__main__':
    main()

