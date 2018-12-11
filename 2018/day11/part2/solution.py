import sys

GRID_SIZE = 300
        
class PowerMap:
    def __init__(self, grid_size, serial_number):
        self.grid_size = grid_size
        self.data = [[[] for y in range(0, grid_size)] for x in range(0, grid_size)]
        for x in range(1, grid_size + 1):
            for y in range(1, grid_size + 1):
                rack_id = x + 10
                power = (rack_id * y + serial_number) * rack_id
                power = int(str(power)[-3]) - 5
                self.data[x - 1][y - 1].append(power)
                
    def calc(self):
        power_by_rect = self.calc_power_of_all_retangles_rooted_at_origin()
                
    def calc_power_of_all_retangles_rooted_at_origin(self):
        power_by_rect = [[0 for y in range(0, self.grid_size)] for x in range(0, self.grid_size)]
        for size in range(1, GRID_SIZE + 1):
            if size == 1:
                power_by_rect[
                
    def get_power(self, x, y, size):
        return self.data[x - 1][y - 1][size]
                
    def set_power(self, x, y, size):
        assert(len(self.data[x - 1][y - 1]) == size - 1)
        self.data[x - 1][y - 1].append(size)
    
power_map = PowerMap(GRID_SIZE, int(sys.argv[1]))
    
power_by_square = populate_single_cells(int(sys.argv[1]))
power_by_row = populate_rows(power_by_square)

for size in range(2, GRID_SIZE + 1):
    print(size)
    for x in range(1, GRID_SIZE - size + 2):
        for y in range(1, GRID_SIZE - size + 2):
            power = 0
            for y1 in range(y, y + size):
                if x == 1:
                    power += power_by_row[y1, x + size - 1]
                else:
                    power += power_by_row[y1, x + size - 1] - power_by_row[y1, x - 1]                   
            power_by_square[x, y, size] = power
        
square_with_most_power = max(power_by_square.keys(), key=lambda s: power_by_square[s])
print(square_with_most_power, power_by_square[square_with_most_power])
        