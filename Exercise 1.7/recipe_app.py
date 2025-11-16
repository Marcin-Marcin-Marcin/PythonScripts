
from sqlalchemy import create_engine, Column
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.types import Integer, String

engine = create_engine("mysql+pymysql://cf-python:password@localhost/task_database")
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

class Recipe(Base):
    __tablename__ = "final_recipes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    ingredients = Column(String(255))
    cooking_time = Column(Integer)
    difficulty = Column(String(20))

    def __repr__(self):
        return f"<Recipe ID: {self.id}-{self.name}-{self.difficulty or 'Unknown'}>"

    def __str__(self):
        line = "-" * 40
        return (
            f"\n{line}\n"
            f"Recipe ID: {self.id}\n"
            f"Recipe Name: {self.name}\n"
            f"Ingredients: {self.ingredients}\n"
            f"Cooking Time: {self.cooking_time} minutes\n"
            f"Difficulty: {self.difficulty}\n"
            f"{line}\n"
        )

    def return_ingredients_as_list(self):
        if not self.ingredients or self.ingredients.strip() == "":
            return []
        return [i.strip() for i in self.ingredients.split(", ") if i.strip()]

    def calculate_difficulty(self):
        num_ingredients = len(self.return_ingredients_as_list())
        if self.cooking_time is None:
            self.difficulty = "Unknown"
            return
        if self.cooking_time < 10 and num_ingredients < 4:
            self.difficulty = "Easy"
        elif self.cooking_time < 10 and num_ingredients >= 4:
            self.difficulty = "Medium"
        elif self.cooking_time >= 10 and num_ingredients < 4:
            self.difficulty = "Intermediate"
        else:
            self.difficulty = "Hard"


Base.metadata.create_all(engine)


def input_non_empty(prompt: str) -> str:
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Please enter a value.")

def input_max_len(prompt: str, max_len: int) -> str:
    while True:
        value = input_non_empty(prompt)
        if len(value) <= max_len:
            return value
        print(f"Please keep it to {max_len} characters or fewer.")

def input_positive_int(prompt: str) -> int:
    while True:
        raw = input_non_empty(prompt)
        if raw.isnumeric():
            n = int(raw)
            if n > 0:
                return n
        print("Please enter a positive whole number.")


def create_recipe():
    name = input_max_len("Enter recipe name (max 50 chars): ", 50)
    cooking_time = input_positive_int("Enter cooking time (minutes): ")

    ing_count = input_positive_int("How many ingredients will you enter? ")
    ings = []
    for i in range(ing_count):
        ing = input_non_empty(f"Ingredient {i+1}: ")
        ings.append(ing)
    ingredients_str = ", ".join(ings)

    recipe_entry = Recipe(
        name=name,
        ingredients=ingredients_str,
        cooking_time=cooking_time,
        difficulty=""
    )
    recipe_entry.calculate_difficulty()
    session.add(recipe_entry)
    session.commit()
    print("\nRecipe created successfully.")
    print(recipe_entry)


def view_all_recipes():
    recipes = session.query(Recipe).all()
    if not recipes:
        print("\nNo recipes found.")
        return None
    for r in recipes:
        print(r)


def search_by_ingredients():
    if session.query(Recipe).count() == 0:
        print("\nNo recipes found.")
        return None

    rows = session.query(Recipe.ingredients).all()
    all_ingredients = []
    for (ing_str,) in rows:
        if not ing_str:
            continue
        for ing in [i.strip() for i in ing_str.split(", ")]:
            if ing and ing not in all_ingredients:
                all_ingredients.append(ing)

    if not all_ingredients:
        print("\nNo ingredients available to search.")
        return None

    print("\nAvailable ingredients:")
    for i, ing in enumerate(all_ingredients, start=1):
        print(f"{i}: {ing}")

    picks = input_non_empty(
        "Enter ingredient numbers separated by spaces: "
    ).split()

    try:
        idxs = [int(p) for p in picks]
    except ValueError:
        print("Please enter only numbers.")
        return None
    if any(i < 1 or i > len(all_ingredients) for i in idxs):
        print("One or more selections were out of range.")
        return None

    search_ingredients = [all_ingredients[i - 1] for i in idxs]

    conditions = [Recipe.ingredients.like(f"%{term}%") for term in search_ingredients]
    results = session.query(Recipe).filter(*conditions).all()

    if not results:
        print("\nNo recipes found with those ingredients.")
        return None

    print("\nMatches:")
    for r in results:
        print(r)


def edit_recipe():
    if session.query(Recipe).count() == 0:
        print("\nNo recipes found.")
        return None

    items = session.query(Recipe.id, Recipe.name).all()
    print("\nAvailable recipes:")
    for rid, rname in items:
        print(f"{rid}: {rname}")

    try:
        rid = int(input_non_empty("Enter the ID to edit: "))
    except ValueError:
        print("Please enter a number.")
        return None

    recipe = session.query(Recipe).filter(Recipe.id == rid).first()
    if not recipe:
        print("No recipe with that ID.")
        return None

    print("\nWhich attribute would you like to edit?")
    print(f"1) Name: {recipe.name}")
    print(f"2) Ingredients: {recipe.ingredients}")
    print(f"3) Cooking time (min): {recipe.cooking_time}")

    choice = input_non_empty("Choose 1/2/3: ")
    if choice not in {"1", "2", "3"}:
        print("Invalid choice.")
        return None

    if choice == "1":
        recipe.name = input_max_len("New name: ", 50)
    elif choice == "2":
        ing_count = input_positive_int("How many ingredients will you enter? ")
        ings = []
        for i in range(ing_count):
            ing = input_non_empty(f"Ingredient {i+1}: ")
            ings.append(ing)
        recipe.ingredients = ", ".join(ings)
    else:
        recipe.cooking_time = input_positive_int("New cooking time (minutes): ")

    recipe.calculate_difficulty()
    session.commit()
    print("\nRecipe updated.")
    print(recipe)


def delete_recipe():
    if session.query(Recipe).count() == 0:
        print("\nNo recipes found.")
        return None

    items = session.query(Recipe.id, Recipe.name).all()
    print("\nAvailable recipes:")
    for rid, rname in items:
        print(f"{rid}: {rname}")

    try:
        rid = int(input_non_empty("Enter the ID to delete: "))
    except ValueError:
        print("Please enter a number.")
        return None

    recipe = session.query(Recipe).filter(Recipe.id == rid).first()
    if not recipe:
        print("No recipe with that ID.")
        return None

    confirm = input_non_empty(
        f"Are you sure you want to delete '{recipe.name}' (ID {recipe.id})? (yes/no): "
    ).strip().lower()
    if confirm in {"y", "yes"}:
        session.delete(recipe)
        session.commit()
        print("Recipe deleted.")
    else:
        print("Deletion cancelled.")


def main():
    while True:
        print("\nWhat would you like to do?")
        print("1) Create a new recipe")
        print("2) View all recipes")
        print("3) Search for recipes by ingredients")
        print("4) Edit a recipe")
        print("5) Delete a recipe")
        print("Type 'quit' to exit.")
        choice = input("Your choice: ").strip().lower()

        if choice == "1":
            create_recipe()
        elif choice == "2":
            view_all_recipes()
        elif choice == "3":
            search_by_ingredients()
        elif choice == "4":
            edit_recipe()
        elif choice == "5":
            delete_recipe()
        elif choice == "quit":
            session.close()
            engine.dispose()
            break
        else:
            print("Please choose 1–5 or type 'quit'.")


if __name__ == "__main__":
    main()
