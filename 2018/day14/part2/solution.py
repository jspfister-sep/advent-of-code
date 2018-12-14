import collections, itertools, sys

def add_new_recipes(recipes, elf1_idx, elf2_idx):
    sum = int(recipes[elf1_idx]) + int(recipes[elf2_idx])
    for digit in str(sum):
        recipes.append(digit)

def get_next_recipe(recipes, elf_idx):
    return (elf_idx + int(recipes[elf_idx]) + 1) % len(recipes)
    
def check_for_scores(recipes, scores_to_find):
    search_length = min(len(recipes), len(scores_to_find) + 1)
    search_start = len(recipes) - search_length
    scores_str = ''.join(list(itertools.islice(recipes, search_start, len(recipes))))
    found_idx = scores_str.find(scores_to_find) 
    if found_idx >= 0:
        return len(recipes) - search_length + found_idx
    return -1

recipes = collections.deque(['3', '7'], 10000000)
scores_to_find = sys.argv[1]
elf1_idx = 0
elf2_idx = 1

while True: 
    add_new_recipes(recipes, elf1_idx, elf2_idx)
    num_recipes = check_for_scores(recipes, scores_to_find)
    if num_recipes >= 0:
        break
    elf1_idx = get_next_recipe(recipes, elf1_idx)
    elf2_idx = get_next_recipe(recipes, elf2_idx)
    print(len(recipes), end='\r')

print(num_recipes)
