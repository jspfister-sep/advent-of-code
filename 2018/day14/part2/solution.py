import sys

NUM_NEXT_SCORES = 10

def add_new_recipes(recipes, elf1_idx, elf2_idx):
    sum = int(recipes[elf1_idx]) + int(recipes[elf2_idx])
    for digit in str(sum):
        recipes += digit
    return recipes

def get_next_recipe(recipes, elf_idx):
    return (elf_idx + int(recipes[elf_idx]) + 1) % len(recipes)
    
def check_for_scores(recipes, scores_to_find):
    search_length = min(len(recipes), len(scores_to_find) * 2 - 1)
    return recipes.rfind(scores_to_find, -search_length)

recipes = '37'
scores_to_find = sys.argv[1]
elf1_idx = 0
elf2_idx = 1

while True: 
    recipes = add_new_recipes(recipes, elf1_idx, elf2_idx)
    num_recipes = check_for_scores(recipes, scores_to_find)
    if num_recipes >= 0:
        break
    elf1_idx = get_next_recipe(recipes, elf1_idx)
    elf2_idx = get_next_recipe(recipes, elf2_idx)

print(num_recipes)
