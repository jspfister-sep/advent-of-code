import itertools, sys

with open(sys.argv[1], 'r') as f:
    ids = f.read().split('\n')
    
for id1, id2 in itertools.combinations(ids, 2):
    diff = list(map(lambda char1, char2: char1 == char2, id1, id2))
    if diff.count(False) == 1:
        diff_index = diff.index(False)
        print(id1)
        print(id2)
        print(id1[:diff_index] + id1[diff_index + 1:])
        break