import math, os

total_fuel = 0

def calculate_module_fuel(weight):
    total_fuel = 0
    remaining_weight = calculate_fuel(weight)
    while remaining_weight > 0:
        total_fuel += remaining_weight
        remaining_weight = calculate_fuel(remaining_weight)
    return total_fuel

def calculate_fuel(weight):
    return math.floor(weight / 3) - 2

with open('data.txt', 'r') as f:
    while True:
        line = f.readline().strip()
        if line:
            total_fuel += calculate_module_fuel(int(line))
        else:
            break

print(total_fuel)

