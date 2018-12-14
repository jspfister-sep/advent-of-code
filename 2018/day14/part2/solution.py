import sys

INITIAL_RECIPES = '37'

class Recipe:
    def __init__(self, score):
        self.score = score
        self.prev = None
        self.next = None

class Scoreboard:
    def __init__(self, initial_recipes):
       self.last = None
       self.num_recipes = 0
       self.elf1 = None
       self.elf2 = None
       self.setup(initial_recipes)

    def add_new_recipes(self):
        sum = int(self.elf1.score) + int(self.elf2.score)
        for digit in str(sum):
            self.append(Recipe(digit))

    def append(self, recipe):
        if not self.last:
            recipe.next = recipe
            recipe.prev = recipe
        else:
            recipe.next = self.last.next
            self.last.next.prev = recipe
            recipe.prev = self.last
            self.last.next = recipe
        self.last = recipe
        self.num_recipes += 1
    
    def check_for_scores(self, scores_to_find):
        search_length = min(self.num_recipes, len(scores_to_find) + 1)
        scores = self.get_last_n_scores(search_length)
        found_idx = scores.rfind(scores_to_find)
        if found_idx >= 0:
            return self.num_recipes - search_length + found_idx
        else:
            return -1
        
    def get_last_n_scores(self, n):
        scores = ''
        recipe = self.last
        while n > 0:
            scores = recipe.score + scores
            recipe = recipe.prev
            n -= 1
        return scores

    def iterate_until_scores_found(self, scores_to_find):
        while True:
            self.add_new_recipes()
            num_recipes = self.check_for_scores(scores_to_find)
            if num_recipes >= 0: 
                return num_recipes 
            self.elf1 = self.update_elf(self.elf1)
            self.elf2 = self.update_elf(self.elf2)

    def setup(self, initial_recipes):
        for r in initial_recipes:
            self.append(Recipe(r))
            if not self.elf2:
                if not self.elf1:
                    self.elf1 = self.last
                else:
                    self.elf2 = self.last

    def update_elf(self, elf):
        num_recipes_to_move = int(elf.score) + 1
        while num_recipes_to_move > 0:
            elf = elf.next
            num_recipes_to_move -= 1
        return elf

scoreboard = Scoreboard(INITIAL_RECIPES) 
num_recipes = scoreboard.iterate_until_scores_found(sys.argv[1])

print(num_recipes)

