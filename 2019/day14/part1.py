import math, re, sys

CHEMICAL_RE = re.compile('(\d+)\s+(\w+),*')

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

    def calculate_required_ore(self):
        required = {}
        available = {}
        stack = [Chemical('FUEL', 1)]
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
    units_of_ore = factory.calculate_required_ore()
    print(f'{units_of_ore} units of ore must be collected '
            'to produce 1 unit of fuel')

if __name__ == '__main__':
    main()
