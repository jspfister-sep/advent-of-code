import sys

BUFFER_SIZE = 1000

def match(unit1, unit2):
    return unit1.swapcase() == unit2
    
def remove_units(stream, index, num_units):
    return stream[:index] + stream[index + num_units:]

def remove_and_reduce(unit_to_remove):
    i = 0
    stream = ''
    with open(sys.argv[1], 'r') as file:
        while(True):
            chunk = file.read(BUFFER_SIZE)
            if chunk:
                stream += chunk
                while i < len(stream) - 1:
                    if stream[i].lower() == unit_to_remove:
                        stream = remove_units(stream, i, 1)
                        i = max(i - 1, 0)
                    elif match(stream[i], stream[i + 1]):
                        stream = remove_units(stream, i, 2)
                        i = max(i - 1, 0)
                    else:
                        i += 1
            else:
                break

    return len(stream)
    
unit = 'a'
lengths = {}

while unit <= 'z':
    lengths[unit] = remove_and_reduce(unit)
    unit = chr(ord(unit) + 1)
    
best_unit = min(lengths.keys(), key=lambda unit: lengths[unit])

print('Removing all {} units allows reduction to {}'.format(best_unit, lengths[best_unit]))
        