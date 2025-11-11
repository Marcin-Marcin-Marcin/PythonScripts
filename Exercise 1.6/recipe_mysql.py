
import sys
import mysql.connector

DB_NAME = "task_database"

def get_connection_and_cursor():
    conn = mysql.connector.connect(
        host="localhost",
        user="cf-python",
        passwd="password",
    )
    cursor = conn.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
    cursor.execute(f"USE {DB_NAME}")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Recipes (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(50) NOT NULL,
            ingredients VARCHAR(255) NOT NULL,
            cooking_time INT NOT NULL,
            difficulty VARCHAR(20) NOT NULL
        )
    """)
    conn.commit()
    return conn, cursor

def calc_difficulty(cooking_time, ingredients_list):
    n = len(ingredients_list)
    if cooking_time < 10 and n < 4:
        return "Easy"
    elif cooking_time < 10 and n >= 4:
        return "Medium"
    elif cooking_time >= 10 and n < 4:
        return "Intermediate"
    else:
        return "Hard"

def list_all_recipes(cursor):
    cursor.execute("SELECT id, name, ingredients, cooking_time, difficulty FROM Recipes ORDER BY id")
    rows = cursor.fetchall()
    if not rows:
        print("\nNo recipes found.\n")
    else:
        print("\nRecipes:")
        for r in rows:
            print("-" * 60)
            print(f"ID: {r[0]}")
            print(f"Name: {r[1]}")
            print(f"Ingredients: {r[2]}")
            print(f"Cooking time (min): {r[3]}")
            print(f"Difficulty: {r[4]}")
        print("-" * 60)
    return rows

def get_name():
    while True:
        name = input("Enter recipe name (≤ 50 chars): ").strip()
        if name and len(name) <= 50:
            return name
        print("Invalid name.")

def get_time():
    while True:
        raw = input("Enter cooking time (minutes, integer): ").strip()
        if raw.isdigit():
            t = int(raw)
            if t >= 0:
                return t
        print("Invalid time.")

def get_ingredients():
    while True:
        raw = input("Enter ingredients (comma-separated): ").strip()
        parts = [p.strip() for p in raw.split(",") if p.strip()]
        if parts:
            return parts
        print("Please enter at least one ingredient.")

def create_recipe(conn, cursor):
    print("\n— Create a new recipe —")
    name = get_name()
    cooking_time = get_time()
    ingredients_list = get_ingredients()
    difficulty = calc_difficulty(cooking_time, ingredients_list)
    ingredients_str = ", ".join(ingredients_list)

    cursor.execute(
        "INSERT INTO Recipes (name, ingredients, cooking_time, difficulty) VALUES (%s, %s, %s, %s)",
        (name, ingredients_str, cooking_time, difficulty),
    )
    conn.commit()
    print("Recipe added.\n")

def search_recipe(conn, cursor):
    print("\n— Search recipes by ingredient —")
    cursor.execute("SELECT ingredients FROM Recipes")
    rows = cursor.fetchall()
    if not rows:
        print("No recipes yet.\n")
        return

    all_ings = set()
    for (ing_str,) in rows:
        for p in ing_str.split(","):
            s = p.strip()
            if s:
                all_ings.add(s)

    options = sorted(all_ings)
    for i, ing in enumerate(options, 1):
        print(f"{i}. {ing}")
    choice = input("Pick an ingredient number: ").strip()
    if not choice.isdigit() or not (1 <= int(choice) <= len(options)):
        print("Invalid choice.\n")
        return
    search_ing = options[int(choice) - 1]

    cursor.execute(
        """
        SELECT id, name, ingredients, cooking_time, difficulty
        FROM Recipes
        WHERE ingredients LIKE %s
        ORDER BY id
        """,
        (f"%{search_ing}%",),
    )
    result = cursor.fetchall()
    if not result:
        print("No matches.\n")
        return
    print(f"\nResults for '{search_ing}':")
    for r in result:
        print("-" * 60)
        print(f"ID: {r[0]}\nName: {r[1]}\nIngredients: {r[2]}\nCooking time: {r[3]}\nDifficulty: {r[4]}")
    print("-" * 60)

def update_recipe(conn, cursor):
    print("\n— Update a recipe —")
    rows = list_all_recipes(cursor)
    if not rows:
        return

    rid_raw = input("Enter ID to update: ").strip()
    if not rid_raw.isdigit():
        print("Invalid ID.\n")
        return
    rid = int(rid_raw)

    cursor.execute("SELECT id, name, ingredients, cooking_time, difficulty FROM Recipes WHERE id = %s", (rid,))
    row = cursor.fetchone()
    if not row:
        print("No recipe with that ID.\n")
        return

    print("What would you like to update?")
    print("1. Name")
    print("2. Cooking time")
    print("3. Ingredients")
    choice = input("Choose 1/2/3: ").strip()

    if choice == "1":
        new_name = get_name()
        cursor.execute("UPDATE Recipes SET name = %s WHERE id = %s", (new_name, rid))
        conn.commit()
        print("Name updated.\n")

    elif choice == "2":
        new_time = get_time()
        ing_list = [p.strip() for p in row[2].split(",") if p.strip()]
        new_diff = calc_difficulty(new_time, ing_list)
        cursor.execute(
            "UPDATE Recipes SET cooking_time = %s, difficulty = %s WHERE id = %s",
            (new_time, new_diff, rid),
        )
        conn.commit()
        print(f"Cooking time updated. Difficulty is now '{new_diff}'.\n")

    elif choice == "3":
        ing_list = get_ingredients()
        ing_str = ", ".join(ing_list)
        current_time = row[3]
        new_diff = calc_difficulty(current_time, ing_list)
        cursor.execute(
            "UPDATE Recipes SET ingredients = %s, difficulty = %s WHERE id = %s",
            (ing_str, new_diff, rid),
        )
        conn.commit()
        print(f"Ingredients updated. Difficulty is now '{new_diff}'.\n")

    else:
        print("Invalid choice.\n")

def delete_recipe(conn, cursor):
    print("\n— Delete a recipe —")
    rows = list_all_recipes(cursor)
    if not rows:
        return

    rid_raw = input("Enter ID to delete: ").strip()
    if not rid_raw.isdigit():
        print("Invalid ID.\n")
        return
    rid = int(rid_raw)

    cursor.execute("SELECT id, name FROM Recipes WHERE id = %s", (rid,))
    row = cursor.fetchone()
    if not row:
        print("No recipe with that ID.\n")
        return

    confirm = input(f"Delete '{row[1]}' (ID {row[0]})? [y/N]: ").strip().lower()
    if confirm != "y":
        print("Cancelled.\n")
        return

    cursor.execute("DELETE FROM Recipes WHERE id = %s", (rid,))
    conn.commit()
    print("Recipe deleted.\n")

def main_menu(conn, cursor):
    while True:
        print("\nMain Menu")
        print("=========================")
        print("1. Create a new recipe")
        print("2. Search for a recipe by ingredient")
        print("3. Update an existing recipe")
        print("4. Delete a recipe")
        print("Type 'quit' to exit.\n")

        choice = input("Your choice: ").strip().lower()
        if choice == "1":
            create_recipe(conn, cursor)
        elif choice == "2":
            search_recipe(conn, cursor)
        elif choice == "3":
            update_recipe(conn, cursor)
        elif choice == "4":
            delete_recipe(conn, cursor)
        elif choice in {"quit", "q", "exit"}:
            print("Saving and exiting…")
            try:
                conn.commit()
            finally:
                conn.close()
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    try:
        conn, cursor = get_connection_and_cursor()
    except mysql.connector.Error as e:
        print("Could not connect to MySQL. Check server and credentials.")
        print(f"MySQL error: {e}")
        sys.exit(1)

    try:
        main_menu(conn, cursor)
    except KeyboardInterrupt:
        print("\nInterrupted. Committing and closing…")
        try:
            conn.commit()
            conn.close()
        except Exception:
            pass
