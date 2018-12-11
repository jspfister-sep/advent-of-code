import re, sys
from operator import attrgetter

class Step:
    def __init__(self, letter, base_duration):
        self.letter = letter
        self.prerequisites = []
        self.dependents = []
        self.progress_secs = 0
        self.secs_to_complete = base_duration + ord(letter) - ord('A') + 1
        
    def add_prerequisite(self, step):
        self.prerequisites.append(step)
        step.dependents.append(self)
        
    def is_done(self):
        return self.progress_secs >= self.secs_to_complete
        
    def is_in_progress(self):
        return self.progress_secs > 0
        
    def is_ready(self):
        return not self.prerequisites and not self.is_in_progress()
        
    def satisfy_prerequisite(self, step):
        self.prerequisites.remove(step)
        
    def work(self):
        self.progress_secs += 1
        if self.is_done():
            for d in self.dependents:
                d.satisfy_prerequisite(self)
        
    def __repr__(self):
        return self.letter
        
    def __str__(self):
        return '{}: {}'.format(self.letter, self.prerequisites)
       
def assign_work(steps, steps_in_progress, num_workers):
    if len(steps_in_progress) < num_workers:
        ready_steps = list(filter(lambda step: step.is_ready(), steps.values()))
        ready_steps = sorted(ready_steps, key=attrgetter('letter'))
        while ready_steps and len(steps_in_progress) < num_workers:
            steps_in_progress.append(ready_steps.pop(0))
        steps_in_progress = sorted(steps_in_progress, key=attrgetter('letter'))
       
def check_for_completed_work(steps, steps_in_progress):
    steps_taken = ''
    for s in steps_in_progress:
        if s.is_done():
            steps_in_progress.remove(s)
            steps_taken += s.letter
            del steps[s.letter]
    return steps_taken

def perform_work(steps_in_progress):
    for s in steps_in_progress:
        s.work()
        
def read_instructions(filename, base_duration):
    steps = {}
    with open(filename, 'r') as file:
        for line in file:
            match = re.match('Step ([A-Z]).+step ([A-Z])', line)
            step1 = steps.setdefault(match.group(1), Step(match.group(1), base_duration))
            step2 = steps.setdefault(match.group(2), Step(match.group(2), base_duration))
            step2.add_prerequisite(step1)
    return steps
    
steps = read_instructions(sys.argv[1], int(sys.argv[2]))
num_workers = int(sys.argv[3])
steps_in_progress = []
steps_taken = ''
elapsed_time = 0

while steps:
    assign_work(steps, steps_in_progress, num_workers)
    perform_work(steps_in_progress)
    steps_taken += check_for_completed_work(steps, steps_in_progress)
    elapsed_time += 1
    
print('Time to completion: {} seconds'.format(elapsed_time))
    