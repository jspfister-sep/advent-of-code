import sys

freq = 0

with open(sys.argv[1], 'r') as file:
    for line in file:
        freq += int(line)

print(freq)