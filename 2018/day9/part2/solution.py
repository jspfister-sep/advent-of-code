import re, sys

class Marble:
    def __init__(self, value, ancestor=None):
        self.value = value
        if not ancestor:
            self.prev = self
            self.next = self
        else:
            self.prev = ancestor
            self.next = ancestor.next
            ancestor.next = self
            self.next.prev = self
            
    def remove(self):
        self.prev.next = self.next
        self.next.prev = self.prev
        
    def scoring_ancestor(self):
        m = self
        for i in range(7):
            m = m.prev
        return m
        
    def __str__(self):
        return str(self.value)

def marble_offset(cur_marble, offset):
    m = cur_marble
    for i in range(abs(offset)):
        m = m.next if offset > 0 else m.prev
    return m

def calc_high_score(num_players, last_marble):
    cur_marble = Marble(0)
    first_marble = cur_marble
    scores = [0] * num_players
    for m in range(1, last_marble + 1):
        if m % 23 == 0:
            cur_marble = cur_marble.scoring_ancestor()
            scores[(m - 1) % num_players] += m + cur_marble.value
            cur_marble.remove()
            cur_marble = cur_marble.next
        else:
            cur_marble = Marble(m, cur_marble.next)
        
    return max(scores)
        
with open(sys.argv[1], 'r') as file:
    for line in file:
        m = re.match('(\d+)\D*(\d+)', line)
        num_players = int(m.group(1))
        last_marble = int(m.group(2))
        high_score = calc_high_score(num_players, last_marble)
        print('Players: {} Last marble: {} High score: {}'.format(num_players, last_marble, high_score))