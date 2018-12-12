import re, sys

class Garden:
    def __init__(self, pots, rules):
        self.pots = pots
        self.rules = rules
        self.rule_size = len(next(iter(rules)))
        self.offset = 0
        
    def iterate(self):
        pots_to_prepend = self.pots_to_pad(self.pots.index('#'))
        self.pots = pots_to_prepend + self.pots
        self.offset -= len(pots_to_prepend)
        self.pots += self.pots_to_pad(len(self.pots) - self.pots.rindex('#') - 1)
        new_pots = '.' * int(self.rule_size / 2)
        for i in range(int(self.rule_size / 2), len(self.pots) - int(self.rule_size / 2)):
            if self.pots[i - 2:i + 3] in self.rules:
                new_pots += self.rules[self.pots[i - 2:i + 3]]
            else:
                new_pots += '.'
        self.pots = new_pots
        self.offset += len(self.pots) - len(self.pots.lstrip('.'))
        self.pots = self.pots.strip('.')

    def pots_to_pad(self, num_empty_pots):
        if num_empty_pots < self.rule_size - 1:
            return '.' * int(self.rule_size - num_empty_pots - 1)
        else:
            return ''
            
    def __str__(self):
        return self.pots

def read_plant_info(file):
    rules = {}
    for line in file:
        m = re.match('initial\sstate\:\s+([.#]+)', line)
        if m:
            pots = m.group(1)
        else:
            m = re.match('([.#]{5})\s=>\s(.|#)', line)
            if m:
                rules[m.group(1)] = m.group(2)
    return pots, rules

with open(sys.argv[1], 'r') as file:
    pots, rules = read_plant_info(file)
    
garden = Garden(pots, rules)

num_generations = int(sys.argv[2])
last_garden = garden.pots
last_offset = garden.offset
for g in range(1, num_generations + 1):
    garden.iterate()
    if garden.pots == last_garden:
        offset_change = garden.offset - last_offset
        print('Generation {} repeats the previous generation with a change in offset of {:+}'.format(g, offset_change))
        garden.offset += (num_generations - g) * offset_change
        break
    else:
        last_garden = garden.pots
        last_offset = garden.offset
    
pot_sum = 0
for i in range(0, len(garden.pots)):
    if garden.pots[i] == '#':
        pot_sum += i + garden.offset
        
print('The sum of the indexes of all pots with plants is {}'.format(pot_sum))
