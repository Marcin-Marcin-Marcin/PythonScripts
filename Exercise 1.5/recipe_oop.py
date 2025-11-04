class Recipe(object):
    all_ingredients = []

    def __init__(self, name):
        self.name = name
        self.ingredients = []
        self.cooking_time = 0
        self.difficulty = None

    def get_name(self):
        return self.name

    def set_name(self, new_name):
        self.name = new_name

    def get_cooking_time(self):
        return self.cooking_time

    def set_cooking_time(self, new_time):
        self.cooking_time = int(new_time)
        self.calculate_difficulty()

    def get_ingredients(self):
        return self.ingredients

    def add_ingredients(self, *items):
        for item in items:
            if item not in self.ingredients:
                self.ingredients.append(item)
        self.calculate_difficulty()
        self.update_all_ingredients()

    def calculate_difficulty(self):
        n = len(self.ingredients)
        t = self.cooking_time
        if t < 10 and n < 4:
            self.difficulty = "Easy"
        elif t < 10 and n >= 4:
            self.difficulty = "Medium"
        elif t >= 10 and n < 4:
            self.difficulty = "Intermediate"
        else:
            self.difficulty = "Hard"
        return self.difficulty

    def get_difficulty(self):
        if self.difficulty is None:
            return self.calculate_difficulty()
        return self.difficulty

    def search_ingredient(self, ingredient):
        return ingredient in self.ingredients

    def update_all_ingredients(self):
        for i in self.ingredients:
            if i not in Recipe.all_ingredients:
                Recipe.all_ingredients.append(i)

    def __str__(self):
        ing = ", ".join(self.ingredients) if self.ingredients else "(none)"
        return (
            f"Recipe Name: {self.name}\n"
            f"Ingredients: {ing}\n"
            f"Cooking Time (minutes): {self.cooking_time}\n"
            f"Difficulty: {self.get_difficulty()}"
        )

    @staticmethod
    def recipe_search(data, search_term):
        found_any = False
        for recipe in data:
            if recipe.search_ingredient(search_term):
                print(recipe, "\n")
                found_any = True
        if not found_any:
            print(f"No recipes found containing: {search_term}\n")


tea = Recipe("Tea")
tea.add_ingredients("Tea Leaves", "Sugar", "Water")
tea.set_cooking_time(5)
print(tea, "\n")

coffee = Recipe("Coffee")
coffee.add_ingredients("Coffee Powder", "Sugar", "Water")
coffee.set_cooking_time(5)
print(coffee, "\n")

cake = Recipe("Cake")
cake.add_ingredients(
    "Sugar", "Butter", "Eggs", "Vanilla Essence",
    "Flour", "Baking Powder", "Milk"
)
cake.set_cooking_time(50)
print(cake, "\n")

banana_smoothie = Recipe("Banana Smoothie")
banana_smoothie.add_ingredients("Bananas", "Milk", "Peanut Butter", "Sugar", "Ice Cubes")
banana_smoothie.set_cooking_time(5)
print(banana_smoothie, "\n")

recipes_list = [tea, coffee, cake, banana_smoothie]

print("--- Recipes containing Water ---")
Recipe.recipe_search(recipes_list, "Water")

print("--- Recipes containing Sugar ---")
Recipe.recipe_search(recipes_list, "Sugar")

print("--- Recipes containing Bananas ---")
Recipe.recipe_search(recipes_list, "Bananas")
