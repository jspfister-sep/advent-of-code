import sys

NUM_NEXT_SCORES = 10

def add_new_recipes(recipes, elf1_idx, elf2_idx):
    sum = recipes[elf1_idx] + recipes[elf2_idx]
    for digit in str(sum):
        recipes.append(int(digit))
    return recipes

def get_next_recipe(recipes, elf_idx):
    return (elf_idx + recipes[elf_idx] + 1) % len(recipes)
    
def next_scores(recipes, current_idx, num_next_scores):
    scores = ''
    for s in recipes[current_idx + 1:current_idx + num_next_scores + 1]:
        scores += str(s)
    return scores

recipes = [3, 7]
max_recipes = int(sys.argv[1])
elf1_idx = 0
elf2_idx = 1

while len(recipes) < max_recipes + NUM_NEXT_SCORES:
    recipes = add_new_recipes(recipes, elf1_idx, elf2_idx)
    elf1_idx = get_next_recipe(recipes, elf1_idx)
    elf2_idx = get_next_recipe(recipes, elf2_idx)

print(next_scores(recipes, max_recipes - 1, NUM_NEXT_SCORES))
