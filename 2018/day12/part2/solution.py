import re, sys

class Garden:
    def __init__(self, pots, rules):
        self.pots = pots
        self.rules = rules
        self.rule_size = len(next(iter(rules)))
        self.offset = 0
        
    def add_empty_pot_padding(self):
        padding = (self.rule_size - 1) * '.'
        self.pots = padding + self.pots + padding
        self.offset -= len(padding)
        
    def grow_to_generation(self, generation):
        last_garden = self.pots
        last_offset = self.offset
        for g in range(1, generation + 1):
            self.iterate()
            if self.pots == last_garden:
                offset_change = self.offset - last_offset
                print('Generation {} is the same as the previous one but with an offset change of {:+}'.format(g, offset_change))
                self.offset += (generation - g) * offset_change
                break
            else:
                last_garden = self.pots
                last_offset = self.offset
        
    def iterate(self):
        self.add_empty_pot_padding()
        new_pots = '.' * int(self.rule_size / 2)
        for i in range(int(self.rule_size / 2), len(self.pots) - int(self.rule_size / 2)):
            if self.pots[i - 2:i + 3] in self.rules:
                new_pots += self.rules[self.pots[i - 2:i + 3]]
            else:
                new_pots += '.'
        self.pots = new_pots
        self.remove_empty_pot_padding()
        
    def remove_empty_pot_padding(self):
        self.offset += len(self.pots) - len(self.pots.lstrip('.'))
        self.pots = self.pots.strip('.')
        
    def sum(self):
        sum = 0
        for i in range(0, len(self.pots)):
            if self.pots[i] == '#':
                sum += i + self.offset
        return sum
            
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
garden.grow_to_generation(int(sys.argv[2]))
        
print(garden.sum())
