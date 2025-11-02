import pickle

def display_recipe(recipe):
    """
    Display a single recipe in a readable format.
    Each recipe is a dictionary with the keys:
    'name', 'cooking_time', 'ingredients', 'difficulty'
    """
    print("\n--------------------------------------")
    print("Recipe Name:", recipe["name"])
    print("Cooking Time (minutes):", recipe["cooking_time"])
    print("Ingredients:", ", ".join(recipe["ingredients"]))
    print("Difficulty:", recipe["difficulty"])
    print("--------------------------------------")


def search_ingredient(data):
    """
    Allow the user to select an ingredient from all_ingredients,
    then show all recipes containing that ingredient.
    """
    all_ingredients = data.get("all_ingredients", [])
    recipes_list = data.get("recipes_list", [])

    if not all_ingredients:
        print("No ingredients found in the data file.")
        return

    print("\nAvailable ingredients:")
    for index, ingredient in enumerate(all_ingredients):
        print(f"{index}: {ingredient}")

    try:
        choice = int(input("\nEnter the number corresponding to the ingredient you want to search for: ").strip())
        ingredient_searched = all_ingredients[choice]
    except (ValueError, IndexError):
        print("Invalid input. Please enter a valid ingredient number.")
    else:
        print(f"\nRecipes containing '{ingredient_searched}':")
        found = False
        for recipe in recipes_list:
            if ingredient_searched in recipe["ingredients"]:
                display_recipe(recipe)
                found = True
        if not found:
            print("No recipes found with that ingredient.")


filename = input("Enter the filename where your recipes are stored (e.g., recipe_binary.bin): ").strip()

try:
    with open(filename, "rb") as file:
        data = pickle.load(file)
except FileNotFoundError:
    print("File not found. Please check the filename and try again.")
except Exception as e:
    print("An unexpected error occurred while reading the file:", e)
else:
    search_ingredient(data)
