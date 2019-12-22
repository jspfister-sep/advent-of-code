import sys
from functools import partial

DECK_SIZE = 10007
EXAMPLE_DECK_SIZE = 10
EXAMPLES = [
        ([
            'deal with increment 7',
            'deal into new stack',
            'deal into new stack',
        ], 
        [0, 3, 6, 9, 2, 5, 8, 1, 4, 7]),
        ([
            'cut 6',
            'deal with increment 7',
            'deal into new stack',
        ], 
        [3, 0, 7, 4, 1, 8, 5, 2, 9, 6]),
        ([
            'deal with increment 7',
            'deal with increment 9',
            'cut -2',
        ],
        [6, 3, 0, 7, 4, 1, 8, 5, 2, 9]),
        ([
            'deal into new stack',
            'cut -2',
            'deal with increment 7',
            'cut 8',
            'cut -4',
            'deal with increment 7',
            'cut 3',
            'deal with increment 9',
            'deal with increment 3',
            'cut -1',
        ],
        [9, 2, 5, 8, 1, 4, 7, 0, 3, 6])
        ]

def cut(n, deck):
    return deck[n:] + deck[:n]

def deal_into_new_stack(deck):
    deck.reverse()
    return deck

def deal_with_increment(n, deck):
    new_deck = [0] * len(deck)
    i = 0
    for c in deck:
        new_deck[i] = c
        i = (i + n) % len(new_deck)
    return new_deck

def generate_deck(size):
    return [i for i in range(size)]

def parse_actions(stream):
    actions = []
    for line in stream:
        line.strip()
        if line.startswith('deal into'):
            action = deal_into_new_stack
        elif line.startswith('deal with'):
            n = parse_trailing_integer(line)
            action = partial(deal_with_increment, n)
        elif line.startswith('cut'):
            n = parse_trailing_integer(line)
            action = partial(cut, n)
        else:
            assert False, 'Bad line!'
        actions.append(action)
    return actions

def parse_trailing_integer(line):
    line = line.split(' ')
    return int(line[-1])

def shuffle(deck, actions):
    for a in actions:
        deck = a(deck)
    return deck

def test():
    pass_count = 0
    for i in range(len(EXAMPLES)):
        example = EXAMPLES[i]
        actions = parse_actions(example[0])
        deck = generate_deck(EXAMPLE_DECK_SIZE)
        deck = shuffle(deck, actions)
        if deck != example[1]:
            print(f'Test {i + 1} failure: expected: {example[1]} actual: {deck}')
        else:
            pass_count += 1
    print(f'{pass_count} tests passed')

def main():
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        test()
    else:
        with open('data.txt', 'r') as f:
            actions = parse_actions(f)
        deck = generate_deck(DECK_SIZE)
        deck = shuffle(deck, actions)
        print(f'Card 2019 is at position {deck.index(2019)}')

if __name__ == '__main__':
    main()

