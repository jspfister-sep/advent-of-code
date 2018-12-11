import sys

GRID_SIZE = 300
SQUARE_SIZE = 3
        
def populate_cells(serial_number):
    cells = {}
    for x in range(1, GRID_SIZE + 1):
        for y in range(1, GRID_SIZE + 1):
            rack_id = x + 10 
            power = (rack_id * y + serial_number) * rack_id
            power = int(str(power)[-3]) - 5
            cells[x, y] = power
    return cells
        
def calculate_square_powers(cells):
    power_by_square = {}
    for x in range(1, GRID_SIZE - SQUARE_SIZE + 1):
        for y in range(1, GRID_SIZE - SQUARE_SIZE + 1):
            power = 0
            for x1 in range(x, x + SQUARE_SIZE):
                for y1 in range(y, y + SQUARE_SIZE):
                    power += cells[x1, y1]
            power_by_square[x, y] = power
    return power_by_square
        
cells = populate_cells(int(sys.argv[1]))
power_by_square = calculate_square_powers(cells)

square_with_most_power = max(power_by_square.keys(), key=lambda s: power_by_square[s])
print(square_with_most_power, power_by_square[square_with_most_power])
        