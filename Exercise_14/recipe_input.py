import pickle

def calc_difficulty(cooking_time, ingredients):
    """
    Return one of: 'Easy', 'Medium', 'Intermediate', 'Hard'
    based on cooking_time (minutes) and number of ingredients.
    """
    num_ing = len(ingredients)
    if cooking_time <= 5 and num_ing <= 4:
        return "Easy"
    elif cooking_time < 10 and num_ing >= 4:
        return "Medium"
    elif cooking_time >= 10 and num_ing < 4:
        return "Intermediate"
    else:
        return "Hard"

def take_recipe():
    """
    Prompt the user for a recipe and return it as a dictionary:
    {
      'name': str,
      'cooking_time': int,
      'ingredients': list[str],
      'difficulty': str
    }
    """
    print("\n— Enter a new recipe —")
    name = input("Recipe name: ").strip()
    cooking_time = int(input("Cooking time (minutes): ").strip())
    ing_raw = input("Ingredients (comma-separated): ").strip()

    ingredients = [i.strip().lower() for i in ing_raw.split(",") if i.strip()]

    difficulty = calc_difficulty(cooking_time, ingredients)
    return {
        "name": name,
        "cooking_time": cooking_time,
        "ingredients": ingredients,
        "difficulty": difficulty
    }

filename = input("Enter the filename to load/save recipes (e.g., recipes.bin): ").strip()

try:
    file = open(filename, "rb")
    data = pickle.load(file)
except FileNotFoundError:
    data = {"recipes_list": [], "all_ingredients": []}
except Exception:
    data = {"recipes_list": [], "all_ingredients": []}
else:
    file.close()
finally:
    recipes_list = data.get("recipes_list", [])
    all_ingredients = data.get("all_ingredients", [])

count = int(input("How many recipes would you like to enter now? ").strip())

for _ in range(count):
    recipe = take_recipe()
    recipes_list.append(recipe)

    for ing in recipe["ingredients"]:
        if ing not in all_ingredients:
            all_ingredients.append(ing)

data = {
    "recipes_list": recipes_list,
    "all_ingredients": all_ingredients
}

with open(filename, "wb") as f:
    pickle.dump(data, f)

print("\nSaved!")
print(f"Total recipes stored: {len(recipes_list)}")
print(f"Total unique ingredients: {len(all_ingredients)}")
