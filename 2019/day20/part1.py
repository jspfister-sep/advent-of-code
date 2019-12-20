from navigation import Direction, Point
import math, sys

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
        distance, _nil = self._dijkstra(self.start, self._get_adjacent_points)
        return distance[self.end]

    def _dijkstra(self, start, get_neighbors):
        open_set = {start}
        previous = {}
        distance = {start: 0}
        visited = set()

        while open_set:
            current = min(open_set, key=lambda p: distance[p])
            if current == self.end:
                break
            open_set.remove(current)
            visited.add(current)
            for n, n_distance in get_neighbors(current, distance[current]):
                if n not in visited and n_distance < distance.setdefault(n, math.inf):
                    distance[n] = n_distance
                    previous[n] = current
                    open_set.add(n)
        return distance, previous

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
        neighbors = []
        for d in Direction:
            neighbor_point = current_point.adjacent(d)
            neighbor_item = self._get_item(neighbor_point)
            if neighbor_item == Item.NAVIGABLE:
                neighbors.append((neighbor_point, current_num_steps + 1))
        if current_point in self.portals:
            neighbors.append((self.portals[current_point], current_num_steps + 1))
        return neighbors

    def _get_item(self, point):
        if point.y < len(self.data) and point.x < len(self.data[0]):
            return Item(self.data[point.y][point.x])
        return Item(Item.WALL)

    def _parse_data(self):
        self.portals = {}
        incomplete_portals = {}
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
                                    self.start = access_point
                                elif item == adjacent_item == Item.END:
                                    self.end = access_point
                                else:
                                    portal_characters = sorted([item, adjacent_item])
                                    portal_name = ''.join(portal_characters)
                                    first_portal_point = incomplete_portals.setdefault(
                                            portal_name,
                                            access_point
                                            )
                                    if first_portal_point != access_point:
                                        self.portals[first_portal_point] = access_point
                                        self.portals[access_point] = first_portal_point

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

