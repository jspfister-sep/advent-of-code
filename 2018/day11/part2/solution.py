import sys, time

GRID_SIZE = 300

class Matrix:
    def __init__(self, size, initial_value):
        self.data = [[initial_value for y in range(0, size)] for x in range(0, size)]
        self.size = size
        
    def get_value(self, x, y):
        return self.data[x - 1][y - 1]
        
    def set_value(self, x, y, value):
        self.data[x - 1][y - 1] = value
        
class PowerMap(Matrix):
    def __init__(self, size, serial_number):
        super().__init__(size, [])
        self.serial_number = serial_number
        self.calc_power_of_all_cells()
        
    def calc_power_of_all_cells(self):
        for x in range(1, self.size + 1):
            for y in range(1, self.size + 1):
                rack_id = x + 10
                power = (rack_id * y + self.serial_number) * rack_id
                power = int(str(power)[-3]) - 5
                self.set_value(x, y, [power])
                
    def calc_power_of_all_retangles_rooted_at_origin(self):
        power_by_rect = Matrix(self.size, 0)
        for size in range(1, self.size + 1):
            if size == 1:
                power_by_rect.set_value(1, 1, self.get_power(1, 1, 1))
            else:
                y = size
                row_power = 0
                for x in range(1, size):
                    top_power = power_by_rect.get_value(x, y - 1)
                    row_power += self.get_power(x, y, 1)
                    power_by_rect.set_value(x, y, top_power + row_power)
                x = size
                column_power = 0
                for y in range(1, size):
                    left_power = power_by_rect.get_value(x - 1, y)
                    column_power += self.get_power(x, y, 1)
                    power_by_rect.set_value(x, y, left_power + column_power)
                top_left_power = power_by_rect.get_value(size - 1, size - 1)
                cell_power = self.get_power(size, size, 1)
                power_by_rect.set_value(size, size, top_left_power + column_power + row_power + cell_power)
        return power_by_rect
                
    def calc_power_of_all_squares(self):
        power_by_rect = self.calc_power_of_all_retangles_rooted_at_origin()
        for x in range(1, self.size + 1):
            for y in range(1, self.size + 1):
                sizes = self.get_value(x, y)
                for size in range(2, min(self.size - x + 2, self.size - y + 2)):
                    origin_rect_power = power_by_rect.get_value(x + size - 1, y + size - 1)
                    left_rect_power = power_by_rect.get_value(x - 1, y + size - 1) if x - 1 > 0 else 0
                    top_rect_power = power_by_rect.get_value(x + size - 1, y - 1) if y - 1 > 0 else 0
                    top_left_rect_power = power_by_rect.get_value(x - 1, y - 1) if x - 1 > 0 and y - 1 > 0 else 0
                    power = (origin_rect_power -
                             left_rect_power -
                             top_rect_power +
                             top_left_rect_power)
                    sizes.append(power)
                self.set_value(x, y, sizes)
            print('Calculating...{}%'.format(int(x / self.size * 100)), end='\r')
        
    def find_square_with_max_power(self):
        self.calc_power_of_all_squares()
        max_x = 0
        max_y = 0
        max_size = 0
        max_power = 0
        for x in range(1, self.size + 1):
            for y in range(1, self.size + 1):
                for size in range(1, len(self.get_value(x, y)) + 1):
                    power = self.get_power(x, y, size)
                    if power > max_power:
                        max_x = x
                        max_y = y
                        max_size = size
                        max_power = power
        return max_x, max_y, max_size, max_power
                    
    def get_power(self, x, y, size):
        return self.get_value(x, y)[size - 1]
    
start_time = time.time()        

x, y, size, power = PowerMap(GRID_SIZE, int(sys.argv[1])).find_square_with_max_power()

print('Found square with highest power in {} seconds:'.format(int(time.time() - start_time)))
print('{},{},{} ({})'.format(x, y, size, power))
