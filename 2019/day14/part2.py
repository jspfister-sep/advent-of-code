import math, re, sys

CHEMICAL_RE = re.compile('(\d+)\s+(\w+),*')
AVAILABLE_ORE = 1000000000000

class Chemical:
    def __init__(self, type, quantity):
        self.type = type
        self.quantity = quantity

    def __repr__(self):
        return f'{self.quantity} {self.type}'

class Reaction:
    def __init__(self, inputs, output):
        self.inputs = inputs
        self.output = output

    def __str__(self):
        return f"{', '.join([str(i) for i in self.inputs])} => {self.output}"

class Factory:
    def __init__(self):
        self.reactions = {}

    def add_reaction(self, reaction):
        self.reactions[reaction.output.type] = reaction

    def calculate_required_ore(self, units_of_fuel):
        required = {}
        available = {}
        stack = [Chemical('FUEL', units_of_fuel)]
        while len(stack) > 0:
            output = stack.pop()
            required.setdefault(output.type, 0)
            available.setdefault(output.type, 0)
            required[output.type] += output.quantity
            if output.type == 'ORE':
                available[output.type] += required[output.type]
            elif required[output.type] > available[output.type]:
                reaction = self.reactions[output.type]
                needed = required[output.type] - available[output.type]
                multiplier = math.ceil(needed / reaction.output.quantity)
                inputs = [Chemical(c.type, c.quantity * multiplier)
                        for c in reaction.inputs]
                stack.extend(inputs)
                available[output.type] += reaction.output.quantity * multiplier
        return required['ORE']

    def calculate_producable_fuel(self, units_of_ore):
        # Assumption: it takes a lot of ore to produce a unit of fuel
        min_fuel = 0
        max_fuel = units_of_ore
        while min_fuel < (max_fuel - 1):
            units_of_fuel = int((min_fuel + max_fuel) / 2)
            ore_required = self.calculate_required_ore(units_of_fuel)
            if ore_required > AVAILABLE_ORE:
                max_fuel = units_of_fuel
            else:
                min_fuel = units_of_fuel
        return min_fuel

    def __str__(self):
        return '\n'.join([str(r) for r in self.reactions.values()])

def parse_input():
    factory = Factory()
    with open(sys.argv[1], 'r') as f:
        for line in f:
            inputs = []
            m = CHEMICAL_RE.findall(line.strip())
            assert m, 'Bad line!'
            o = m.pop()
            output = Chemical(o[1], int(o[0]))
            for i in m:
                inputs.append(Chemical(i[1], int(i[0])))
            factory.add_reaction(Reaction(inputs, output))
    return factory

def main():
    factory = parse_input()
    producable_fuel = factory.calculate_producable_fuel(AVAILABLE_ORE)

    print(f'{producable_fuel} units of fuel can be produced with {AVAILABLE_ORE} '
            'units of ore')

if __name__ == '__main__':
    main()
