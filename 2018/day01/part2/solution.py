import sys

with open(sys.argv[1], 'r') as file:
    freq_deltas = list(map(lambda x: int(x), file.read().split('\n')))

found_repeat = False
cur_freq = 0
# Add starting frequency to list of previous frequencies,
# using dictionary for performance
prev_freqs = {cur_freq : None}

while(not found_repeat):
    for cur_delta in freq_deltas:
        cur_freq += cur_delta
        if cur_freq in prev_freqs.keys():
            found_repeat = True
            break
        else:
            prev_freqs[cur_freq] = None
            
print(cur_freq)