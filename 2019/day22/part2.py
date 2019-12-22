import sys
from functools import partial

FINAL_INDEX = 2020
DECK_SIZE = 119315717514047 
NUM_SHUFFLES = 101741582076661
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

def calculate_linear_coefficients(deck_size, actions):
    # Observe: All operations are linear for indices inside the deck
    # let f(i) be the function that computes the original index that is
    #   tranformed into i by one iteration of the shuffle (i.e. puzzle input)
    # f(i) = a * i + b
    # f(0) = a * 0 + b = b => b = f(0)
    # f(1) = a + b => a = f(1) - b
    b = reverse_shuffle(deck_size, 0, actions)
    a = reverse_shuffle(deck_size, 1, actions) - b
    return a, b

def calculate_original_index(index, deck_size, num_iterations, actions):
    # f(i) = a * i + b
    # f^2(i) = a(a * i + b) + b = a^2 * i + ab + b
    # f^3(i) = a(a^2 * i + ab + b) + b = a^3 * i + a^2 * b + ab + b
    # f^n(i) = a^n * i + a^(n - 1) * b + a(n - 2) * b + ... + b
    #        = a^n * i + (a^n - 1)/(a - 1) * b
    # I'm not entirely sure how we get from that to this, but it kind of
    #   makes sense:
    # f^n(i) = ((a^n % d) * i + (a^n % d) * modinv(a - 1, d) * b) % d
    # See documentation for pow(). Without it's built-in mod support with
    #   increased performance, it would take forever to compute and might also
    #   cause an overflow. pow() can also compute modular inverses when the
    #   exponent is negative (Python 3.8+)
    a, b = calculate_linear_coefficients(deck_size, actions)
    n = num_iterations
    d = deck_size
    i = index
    return (pow(a, n, d) * i + (pow(a, n, d) - 1) * pow(a - 1, -1, d) * b) % d

def parse_actions_reverse(stream):
    actions = []
    for line in stream:
        line.strip()
        if line.startswith('deal into'):
            action = reverse_deal_into_new_stack
        elif line.startswith('deal with'):
            n = parse_trailing_integer(line)
            action = partial(reverse_deal_with_increment, n)
        elif line.startswith('cut'):
            n = parse_trailing_integer(line)
            action = partial(reverse_cut, n)
        else:
            assert False, 'Bad line!'
        actions.insert(0, action)
    return actions

def parse_trailing_integer(line):
    line = line.split(' ')
    return int(line[-1])

def reverse_cut(n, deck_size, index):
    return (index + n + deck_size) % deck_size

def reverse_deal_into_new_stack(deck_size, index):
    return deck_size - index - 1

def reverse_deal_with_increment(n, deck_size, index):
    return (pow(n, -1, deck_size) * index) % deck_size

def reverse_shuffle(deck_size, index, actions):
    for a in actions:
        index = a(deck_size, index)
    return index

def test():
    pass_count = 0
    for i in range(len(EXAMPLES)):
        example = EXAMPLES[i]
        deck_size = len(example[1])
        actions = parse_actions_reverse(example[0])
        for j in range(deck_size):
            original_index = reverse_shuffle(deck_size, j, actions)
            if original_index != example[1][j]:
                print(f'Test {i + 1}:{j + 1} failure: ' 
                    f'expected: {example[1][j]} actual: {original_index}')
            else:
                pass_count += 1
    print(f'{pass_count} tests passed')

def main():
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        test()
    else:
        with open('data.txt', 'r') as f:
            actions = parse_actions_reverse(f)
        original_index = calculate_original_index(
                FINAL_INDEX,
                DECK_SIZE,
                NUM_SHUFFLES,
                actions)
        print(f'The card at position {FINAL_INDEX} is {original_index}')

if __name__ == '__main__':
    main()

