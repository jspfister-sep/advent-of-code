import re, sys

def index_offset(cur_idx, offset, size):
    if offset < 0:
        return size - ((size - cur_idx - 1 - offset) % size) - 1
    else:
        return (cur_idx + offset) % size

def calc_high_score(num_players, last_marble):
    m_index = 0
    marbles = [0]
    p_index = 0
    scores = [0] * num_players
    for m in range(1, last_marble + 1):
        if m % 23 == 0:
            m_index = index_offset(m_index, -7, len(marbles))
            scores[p_index] += m + marbles[m_index]
            marbles = marbles[:m_index] + marbles[m_index + 1:]
        else:
            m_index = index_offset(m_index, 2, len(marbles))
            marbles.insert(m_index, m)
        p_index = (p_index + 1) % num_players
        
    return max(scores)
        
with open(sys.argv[1], 'r') as file:
    for line in file:
        m = re.match('(\d+)\D*(\d+)', line)
        num_players = int(m.group(1))
        last_marble = int(m.group(2))
        high_score = calc_high_score(num_players, last_marble)
        print('Players: {} Last marble: {} High score: {}'.format(num_players, last_marble, high_score))