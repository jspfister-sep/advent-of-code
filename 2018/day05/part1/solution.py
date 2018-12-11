import sys

BUFFER_SIZE = 1000

def match(unit1, unit2):
    return unit1.swapcase() == unit2
    
def remove_pair(stream, index):
    return stream[:index] + stream[index + 2:]

i = 0
stream = ''
    
with open(sys.argv[1], 'r') as file:
    while(True):
        chunk = file.read(BUFFER_SIZE)
        if chunk:
            stream += chunk
            while i < len(stream) - 1:
                if match(stream[i], stream[i + 1]):
                    stream = remove_pair(stream, i)
                    i = max(i - 1, 0)
                else:
                    i += 1
        else:
            break

print(len(stream))
        