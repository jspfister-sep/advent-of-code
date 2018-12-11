import re, sys

MIN_NUMBER_OF_CLAIMS = 2

def get_points_in_rectangle(line):
    points = []
    m = re.match('\#[0-9]+\s+\@\s+([0-9]+),([0-9]+)\:\s+([0-9]+)x([0-9]+)', line)
    x1 = int(m.group(1)) + 1
    y1 = int(m.group(2)) + 1
    x2 = x1 + int(m.group(3))
    y2 = y1 + int(m.group(4))
    for x in range(x1, x2):
        for y in range (y1, y2):
            points.append((x, y))
    return points

claimed_counts = {}

with open(sys.argv[1], "r") as file:
    for line in file:
        for point in get_points_in_rectangle(line):
            if point in claimed_counts.keys():
                claimed_counts[point] += 1
            else:
                claimed_counts[point] = 1

print(len(list(filter(lambda claim_count: claim_count >= MIN_NUMBER_OF_CLAIMS, claimed_counts.values()))))            
