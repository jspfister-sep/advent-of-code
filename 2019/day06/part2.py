import math
import sys

class OrbitObject:
    def __init__(self, name):
        self.name = name
        self.neighbors = []
        self.visited = False
        self.distance = math.inf

def read_input():
    with open(sys.argv[1], 'r') as f:
        objects = {}
        while True:
            line = f.readline()
            if not line:
                break
            current_objects = line.strip().split(')')
            orbitee_name = current_objects[0]
            orbiter_name = current_objects[1]
            orbitee = objects.setdefault(orbitee_name, OrbitObject(orbitee_name))
            orbiter = objects.setdefault(orbiter_name, OrbitObject(orbiter_name))
            orbitee.neighbors.append(orbiter)
            orbiter.neighbors.append(orbitee)
    return objects

objects = read_input()
you = objects.pop('YOU')
remaining_objects = list(objects.values())
you.distance = 0
remaining_objects.append(you)
santa = None

while len(remaining_objects) > 0:
    current_object = min(remaining_objects, key=lambda o: o.distance)
    remaining_objects.remove(current_object)
    for n in [n for n in current_object.neighbors if not n.visited]:
        n.distance = min(n.distance, current_object.distance + 1)
    current_object.visited = True
    if current_object.name == 'SAN':
        santa = current_object
        break

if santa:
    print(f'There are {santa.distance - 2} orbital transfers between you and Santa')
else:
    print('No path found between you and Santa!')