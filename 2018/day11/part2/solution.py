import sys

GRID_SIZE = 300
        
def populate_single_cells(serial_number):
    power_by_square = {}
    for x in range(1, GRID_SIZE + 1):
        for y in range(1, GRID_SIZE + 1):
            rack_id = x + 10 
            power = (rack_id * y + serial_number) * rack_id
            power = int(str(power)[-3]) - 5
            power_by_square[x, y, 1] = power
    return power_by_square
    
def populate_rows(grid):
    power_by_row = {}
    for row in range(1, GRID_SIZE + 1):
        for size in range(1, GRID_SIZE + 1):
            if size == 1:
                power_by_row[row, size] = grid[1, row, 1]
            else:
                power_by_row[row, size] = power_by_row[row, size - 1] + grid[size, row, 1]
    return power_by_row
    
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
        