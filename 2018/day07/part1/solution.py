import re, sys
from operator import attrgetter

class Step:
    def __init__(self, letter):
        self.letter = letter
        self.prerequisites = []
        self.dependents = []
        
    def add_prerequisite(self, step):
        self.prerequisites.append(step)
        step.dependents.append(self)
        
    def satisfy_prerequisite(self, step):
        self.prerequisites.remove(step)
        
    def is_ready(self):
        return not self.prerequisites
        
    def take(self):
        for d in self.dependents:
            d.satisfy_prerequisite(self)
        
    def __repr__(self):
        return self.letter
        
    def __str__(self):
        return '{}: {}'.format(self.letter, self.prerequisites)
       
def read_instructions(filename):
    steps = {}
    with open(filename, 'r') as file:
        for line in file:
            match = re.match('Step ([A-Z]).+step ([A-Z])', line)
            step1 = steps.setdefault(match.group(1), Step(match.group(1)))
            step2 = steps.setdefault(match.group(2), Step(match.group(2)))
            step2.add_prerequisite(step1)
    return steps
        
steps = read_instructions(sys.argv[1])
steps_taken = ''

while steps:
    ready_steps = list(filter(lambda s: s.is_ready(), steps.values()))
    next_step = sorted(ready_steps, key=attrgetter('letter'))[0]
    next_step.take()
    steps_taken += next_step.letter
    del steps[next_step.letter]
    
print(steps_taken)
    