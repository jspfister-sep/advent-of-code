import sys

class OrbitObject:
    def __init__(self, name):
        self.name = name
        self.orbiters = []
        self.num_indirect_orbiters = 0
        self.visited = False

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
            orbitee.orbiters.append(orbiter)
    return objects

objects = read_input()
stack = list(objects.values())

while len(stack) > 0:
    o = stack.pop()
    if not o.visited:
        unvisited_orbiters = [r for r in o.orbiters if not r.visited]
        if unvisited_orbiters:
            stack.append(o)
            stack.extend(unvisited_orbiters)
        else:
            orbiter_sums = [len(r.orbiters) + r.num_indirect_orbiters for r in o.orbiters]
            o.num_indirect_orbiters = sum(orbiter_sums)
            o.visited = True

num_direct_orbits = 0
num_indirect_orbits = 0

for o in objects.values():
    num_direct_orbits += len(o.orbiters)
    num_indirect_orbits += o.num_indirect_orbiters

print(f'There are {num_direct_orbits} direct orbits '
    f'and {num_indirect_orbits} indirect orbits, '
    f'totalling {num_direct_orbits + num_indirect_orbits} orbits.')

