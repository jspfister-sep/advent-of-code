import sys

repeat2_count = 0
repeat3_count = 0

with open(sys.argv[1], 'r') as file:
    for id in file:
        counts = list(map(lambda x: id.count(x), set(id)))
        repeat2_count += (1 if 2 in counts else 0)
        repeat3_count += (1 if 3 in counts else 0)
        
print('{} x {} = {}'.format(repeat2_count, repeat3_count, repeat2_count * repeat3_count))