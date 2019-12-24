import sys

SIZE = 5
BUG = '#'
SPACE = '.'

def get_next_state(state):
    new_state = ''
    for i in range(len(state)):
        num_adjacent_bugs = 0
        if has_bug_above(state, i):
            num_adjacent_bugs += 1
        if has_bug_below(state, i):
            num_adjacent_bugs += 1
        if has_bug_left(state, i):
            num_adjacent_bugs += 1
        if has_bug_right(state, i):
            num_adjacent_bugs += 1
        if is_bug(state, i):
            if num_adjacent_bugs == 1:
                new_state +='1'
            else:
                new_state +='0'
        elif 1 <= num_adjacent_bugs <= 2:
            new_state +='1'
        else:
            new_state +='0'
    return new_state

def has_bug_above(state, index):
    if index + SIZE < len(state):
        return state[index + SIZE] == '1'
    return False

def has_bug_below(state, index):
    if index - SIZE >= 0:
        return state[index - SIZE] == '1'
    return False

def has_bug_left(state, index):
    if (index + 1) % SIZE == 0:
        return False
    return state[index + 1] == '1'

def has_bug_right(state, index):
    if index % SIZE == 0:
        return False
    return state[index - 1] == '1'

def is_bug(state, index):
    return state[index] == '1'

def print_state(state):
    for i in range(len(state) - 1, -1, -1):
        if state[i] == '1':
            print(BUG, end='')
        else:
            print(SPACE, end='')
        if i % SIZE == 0:
            print('')

def read_state_from_file(filename):
    with open(filename, 'r') as f:
        initial_value = ''
        for line in f:
            line = line.strip()
            line = line.replace(SPACE, '0')
            line = line.replace(BUG, '1')
            line = line[::-1]
            initial_value = line + initial_value
    return initial_value

def main():
    state = read_state_from_file(sys.argv[1])
    previous_states = set()
    while True:
        state_as_int = int(state, 2)
        if state_as_int in previous_states:
            break
        previous_states.add(state_as_int)
        state = get_next_state(state)

    print('The first state to repeat is:')
    print_state(state)
    print(f'Its biodiversity rating is {state_as_int}')

if __name__ == '__main__':
    main()

