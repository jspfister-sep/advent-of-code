import math, sys

width = int(sys.argv[1])
height = int(sys.argv[2])
layer_size = width * height
min_num_zeros = math.inf
min_zero_layer = math.inf
min_zero_layer_data = ''
layer_count = 0

with open(sys.argv[3], 'r') as f:
    while True:
        layer_data = f.read(layer_size)
        if len(layer_data) < layer_size:
            break
        num_zeros = layer_data.count('0')
        if num_zeros < min_num_zeros:
            min_num_zeros = num_zeros
            min_zero_layer = layer_count
            min_zero_layer_data = layer_data
        layer_count += 1

one_count = min_zero_layer_data.count('1')
two_count = min_zero_layer_data.count('2')

print(f'Layer {min_zero_layer + 1} has the fewest zeroes ({min_num_zeros}).\n'
        f'It also has {one_count} ones and {two_count} twos. '
        f'{one_count} * {two_count} = {one_count * two_count}')
