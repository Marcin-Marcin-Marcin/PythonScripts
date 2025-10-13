recipes_list = []
ingredients_list = []

def take_recipe():
    name = input("Enter recipe name: ").strip()

    while True:
        try:
            cooking_time = int(input("Enter cooking time (minutes): ").strip())
            break
        except ValueError:
            print("Please enter a whole number for minutes.")

    print("Enter ingredients (one per line). Press Enter on an empty line to finish.")
    ingredients = []
    while True:
        item = input("Ingredient: ").strip()
        if item == "":
            break
        ingredients.append(item)

    return {
        "name": name,
        "cooking_time": cooking_time,
        "ingredients": ingredients,
    }

while True:
    try:
        n = int(input("How many recipes would you like to enter? ").strip())
        if n < 0:
            print("Please enter a non-negative number.")
            continue
        break
    except ValueError:
        print("Please enter a whole number.")

for _ in range(n):
    recipe = take_recipe()

    for ingredient in recipe["ingredients"]:
        if ingredient not in ingredients_list:
            ingredients_list.append(ingredient)

    recipes_list.append(recipe)

for recipe in recipes_list:
    name = recipe["name"]
    ct = recipe["cooking_time"]
    ing = recipe["ingredients"]
    num_ing = len(ing)

    if ct < 10 and num_ing < 4:
        difficulty = "Easy"
    elif ct < 10 and num_ing >= 4:
        difficulty = "Medium"
    elif ct >= 10 and num_ing < 4:
        difficulty = "Intermediate"
    else:
        difficulty = "Hard"

    print(f"\nRecipe: {name}")
    print(f"Cooking Time (min): {ct}")
    print("Ingredients:")
    for item in ing:
        print(item)
    print(f"Difficulty level: {difficulty}")

print("\nIngredients Available Across All Recipes")
print("----------------------------------------")
for item in sorted(ingredients_list, key=str.lower):
    print(item)

print("\nPrinted ingredient list.")