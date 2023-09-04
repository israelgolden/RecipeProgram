import os
import datetime
import subprocess  # Import the subprocess module for opening files

# Define a dictionary to store the shopping list categorized by ingredient categories.
shopping_list = {}

# Define a dictionary to store the recipes, their ingredients, and associated URLs.
# Save some time: {"ingredient": "", "unit": "", "quantity": , "category": ""},
recipes = {
    "Buttermilk Green Goddess Slaw": {
        "ingredients": [
            {"ingredient": "avocado", "unit": "null", "quantity": 1, "category": "Produce"},
            {"ingredient": "buttermilk", "unit": "cup", "quantity": 0.75, "category": "Dairy"},
            {"ingredient": "lemon", "unit": "null", "quantity": 1, "category": "Produce"},
            {"ingredient": "oil-packed anchovy filet", "unit": "null", "quantity": 2, "category": "Canned Goods"},
            {"ingredient": "scallion", "unit": "null", "quantity": 2, "category": "Produce"},
            {"ingredient": "garlic", "unit": "cloves", "quantity": 1, "category": "Produce"},
            {"ingredient": "Italian parsley", "unit": "null", "quantity": 1, "category": "Produce"},
            {"ingredient": "chives", "unit": "tbsp", "quantity": 3, "category": "Produce"},
            {"ingredient": "tarragon", "unit": "leaves", "quantity": 2, "category": "Produce"},
            {"ingredient": "olive oil", "unit": "tbsp", "quantity": 2, "category": "Condiments & Spices"},
            {"ingredient": "basil leaves", "unit": "tbsp", "quantity": 1, "category": "Produce"},
            {"ingredient": "green cabbage", "unit": "cup", "quantity": 4, "category": "Produce"},
            {"ingredient": "scallions", "unit": "null", "quantity": 4, "category": "Produce"},
            {"ingredient": "jalapeno", "unit": "null", "quantity": 1, "category": "Produce"},
            {"ingredient": "cilantro", "unit": "cup", "quantity": 0.25, "category": "Produce"},
        ],
        "url": "https://cooking.nytimes.com/recipes/1023266-buttermilk-green-goddess-slaw?action=click&module=Collection%20Page%20Recipe%20Card&region=Sam%20Sifton%E2%80%99s%20Suggestions&pgType=collection&rank=5",
        "Type": "Side",
        "Servings": 6,
        "Kcal/Serving": 149,
    },
    "Tomato Bruschetta": {
        "ingredients": [
            {"ingredient": "plum tomatoes", "unit": "pound", "quantity": 1, "category": "Produce"},
            {"ingredient": "olive oil", "unit": "tbsp", "quantity": 5, "category": "Condiments & Spices"},
            {"ingredient": "garlic", "unit": "cloves", "quantity": 2, "category": "Produce"},
            {"ingredient": "basil", "unit": "leaves", "quantity": 8, "category": "Produce"},
            {"ingredient": "Italian bread", "unit": "loaf", "quantity": 1, "category": "Bread & Bakery"},
        ],
        "url": "https://cooking.nytimes.com/recipes/1020272-tomato-bruschetta",
        "Type": "Side",
        "Servings": 4,
        "Kcal/Serving": 177
    },
    "Mushroom Stroganoff with Mashed Potatoes": {
        "ingredients": [
            {"ingredient": "olive oil", "unit": "tbsp", "quantity": 2, "category": "Condiments & Spices"},
            {"ingredient": "yellow onion", "unit": "null", "quantity": 1, "category": "Produce"},
            {"ingredient": "mixed mushrooms", "unit": "pound", "quantity": 1.5, "category": "Produce"},
            {"ingredient": "fresh thyme", "unit": "sprig", "quantity": 2, "category": "Produce"},
            {"ingredient": "garlic", "unit": "cloves", "quantity": 2, "category": "Produce"},
            {"ingredient": "dry white wine", "unit": "cup", "quantity": 0.5, "category": "Beverages"},
            {"ingredient": "vegetable stock", "unit": "cup", "quantity": 1, "category": "Soups, Sauces, and Gravies"},
            {"ingredient": "soy sauce", "unit": "tbsp", "quantity": 2, "category": "Condiments & Spices"},
            {"ingredient": "Dijon mustard", "unit": "tsp", "quantity": 1.5, "category": "Condiments & Spices"},
            {"ingredient": "creme fraiche", "unit": "cup", "quantity": 0.5, "category": "Dairy"},
            {"ingredient": "sweet paprika", "unit": "tbsp", "quantity": 1, "category": "Condiments & Spices"},
            {"ingredient": "Italian parsley", "unit": "null", "quantity": 1, "category": "Produce"},
            {"ingredient": "russet potatoes", "unit": "pound", "quantity": 3, "category": "Produce"},
            {"ingredient": "whole milk", "unit": "cup", "quantity": 1.5, "category": "Dairy"},
            {"ingredient": "unsalted butter", "unit": "tbsp", "quantity": 4, "category": "Dairy"},
        ],
        "url": "https://cooking.nytimes.com/recipes/1022724-mushroom-stroganoff",
        "Type": "Main",
        "Servings": 4,
        "Kcal/Serving": 495
    },
    "Rice Noodles With Spicy Pork and Herbs": {
        "ingredients": [
            {"ingredient": "round rice noodles", "unit": "pound", "quantity": 1, "category": "Pasta, Rice & Cereal"},
            {"ingredient": "rice vinegar", "unit": "tbsp", "quantity": 2, "category": "Condiments & Spices"},
            {"ingredient": "black vinegar", "unit": "tbsp", "quantity": 1, "category": "Condiments & Spices"},
            {"ingredient": "chile oil", "unit": "tbsp", "quantity": 1, "category": "Condiments & Spices"},
            {"ingredient": "sugar", "unit": "tsp", "quantity": 1, "category": "Condiments & Spices"},
            {"ingredient": "canola oil", "unit": "tbsp", "quantity": 1, "category": "Condiments & Spices"},
            {"ingredient": "pork", "unit": "pound", "quantity": 0.5, "category": "Protein"},
            {"ingredient": "garlic", "unit": "cloves", "quantity": 2, "category": "Produce"},
            {"ingredient": "ginger", "unit": "tbsp", "quantity": 1, "category": "Produce"},
            {"ingredient": "scallion", "unit": "null", "quantity": 2, "category": "Produce"},
            {"ingredient": "yacai - Sichuan preserved vegetables", "unit": "tbsp", "quantity": 1, "category": "Canned Goods"},
            {"ingredient": "basil", "unit": "leaves", "quantity": 8, "category": "Produce"},
            {"ingredient": "salted, roasted peanuts", "unit": "cup", "quantity": 0.25, "category": "Snacks"},
            {"ingredient": "breakfast radish", "unit": "null", "quantity": 4, "category": "Produce"},

        ],
            "url": "https://cooking.nytimes.com/recipes/1018852-rice-noodles-with-spicy-pork-and-herbs",
            "Type": "Main",
            "Servings": 4,
            "Kcal/Serving": 311
    },
    "Stone Fruit Caprese": {
        "ingredients": [
            {"ingredient": "stone fruit", "unit": "pound", "quantity": 2, "category": "Produce"},
            {"ingredient": "lemon", "unit": "null", "quantity": 1, "category": "Produce"},
            {"ingredient": "sugar", "unit": "tsp", "quantity": 2, "category": "Condiments & Spices"},
            {"ingredient": "fresh mozzarella", "unit": "oz", "quantity": 8, "category": "Dairy"},
            {"ingredient": "basil", "unit": "leaves", "quantity": 20, "category": "Produce"},
            {"ingredient": "olive oil", "unit": "tbsp", "quantity": 2, "category": "Condiments & Spices"},
        ],
        "url": "https://cooking.nytimes.com/recipes/1023336-stone-fruit-caprese",
        "Type": "Side",
        "Servings": 4,
        "Kcal/Serving": 300
    },    
    "Stuffed Peppers": {
        "ingredients": [
            {"ingredient": "red, orange, or yellow bell peppers", "unit": "null", "quantity": 4, "category": "Produce"},
            {"ingredient": "olive oil", "unit": "tbsp", "quantity": 2, "category": "Condiments & Spices"},
            {"ingredient": "fennel bulb", "unit": "null", "quantity": 1, "category": "Produce"},
            {"ingredient": "yellow onion", "unit": "null", "quantity": 1, "category": "Produce"},
            {"ingredient": "garlic", "unit": "cloves", "quantity": 3, "category": "Produce"},
            {"ingredient": "dried oregano", "unit": "tsp", "quantity": 1, "category": "Condiments & Spices"},
            {"ingredient": "red-pepper flakes", "unit": "tsp", "quantity": 0.5, "category": "Condiments & Spices"},
            {"ingredient": "ground beef", "unit": "pound", "quantity": 1, "category": "Protein"},
            {"ingredient": "chicken broth", "unit": "cup", "quantity": 0.75, "category": "Soups, Sauces, and Gravies"},
            {"ingredient": "canned diced fire-roasted tomatoes", "unit": "oz", "quantity": 14, "category": "Canned Goods"},
            {"ingredient": "white rice", "unit": "cup", "quantity": 1, "category": "Pasta, Rice & Cereal"},
            {"ingredient": "parmesan", "unit": "cup", "quantity": 0.25, "category": "Dairy"},
            {"ingredient": "Italian parsley", "unit": "tbsp", "quantity": 2, "category": "Produce"},
            {"ingredient": "shredded mozzarella", "unit": "cup", "quantity": 1, "category": "Dairy"},
        ],
        "url": "https://cooking.nytimes.com/recipes/1021007-stuffed-peppers",
        "Type": "Main",
        "Servings": 6,
        "Kcal/Serving": 320
    },  
    "Shrimp Scampi With Orzo": {
        "ingredients": [
            {"ingredient": "large shrimp, peeled and deveined", "unit": "pound", "quantity": 1, "category": "Fish & Seafood"},
            {"ingredient": "olive oil", "unit": "tbsp", "quantity": 3, "category": "Condiments & Spices"},
            {"ingredient": "lemon", "unit": "null", "quantity": 1, "category": "Produce"},
            {"ingredient": "red-pepper flakes", "unit": "tsp", "quantity": 0.5, "category": "Condiments & Spices"},
            {"ingredient": "garlic", "unit": "cloves", "quantity": 4, "category": "Produce"},
            {"ingredient": "unsalted butter", "unit": "tbsp", "quantity": 2, "category": "Dairy"},
            {"ingredient": "orzo", "unit": "cup", "quantity": 1, "category": "Pasta, Rice & Cereal"},
            {"ingredient": "dry white wine", "unit": "cup", "quantity": 0.3, "category": "Beverages"},
            {"ingredient": "chicken stock", "unit": "cup", "quantity": 2, "category": "Soups, Sauces, and Gravies"},
            {"ingredient": "Italian parsley", "unit": "tbsp", "quantity": 3, "category": "Produce"},
        ],
        "url": "https://cooking.nytimes.com/recipes/1020330-shrimp-scampi-with-orzo",
        "Type": "Main",
        "Servings": 4,
        "Kcal/Serving": 364
    }, 
}

# Function to add ingredients from a recipe to the shopping list.
def add_recipe_to_shopping_list(recipe_name):
    recipe_data = recipes.get(recipe_name, {})
    if not recipe_data:
        print("Recipe not found. Please enter a valid recipe.")
        return

    ingredients = recipe_data.get("ingredients", [])
    for ingredient in ingredients:
        category = ingredient["category"]
        ingredient_name = ingredient["ingredient"]
        unit = ingredient["unit"]
        quantity = ingredient["quantity"]

        if category not in shopping_list:
            shopping_list[category] = []

        # Check if the ingredient already exists in the shopping list.
        existing_ingredient = next((item for item in shopping_list[category] if ingredient_name in item), None)

        if existing_ingredient:
            # If the ingredient exists, update its quantity.
            existing_quantity = float(existing_ingredient.split()[0])
            updated_quantity = existing_quantity + quantity
            formatted_quantity = f"{updated_quantity:.2f}" if updated_quantity < 1 else f"{int(updated_quantity)}"
            shopping_list[category].remove(existing_ingredient)
            shopping_list[category].append(f"{formatted_quantity} {unit if unit != 'null' else ''} {ingredient_name}")
        else:
            # If the ingredient doesn't exist, add it to the shopping list.
            formatted_quantity = f"{quantity:.2f}" if quantity < 1 else f"{int(quantity)}"
            shopping_list[category].append(f"{formatted_quantity} {unit if unit != 'null' else ''} {ingredient_name}")

# Function to display the shopping list categorized by ingredient categories.
def display_shopping_list(selected_recipes):
    print("Shopping List:")
    for category, items in shopping_list.items():
        print(category + ":")
        for item in items:
            print("- " + item)

    # Display selected recipes.
    print("\nSelected Recipes:")
    for recipe_name in selected_recipes:
        print("- " + recipe_name)

    # Display recipe URLs as hyperlinks at the bottom of the page.
    print("\nSelected Recipe Links:")
    for recipe_name in selected_recipes:
        recipe_data = recipes.get(recipe_name)
        if recipe_data:
            recipe_url = recipe_data.get("url")
            if recipe_url:
                print(f"- [{recipe_name}]({recipe_url})")

# Function to save the selected recipes and their links to a .txt file with a timestamp in a specified directory.
def save_selected_recipes_to_file(directory, selected_recipes):
    today_date = datetime.date.today().strftime("%Y-%m-%d")
    file_name = f"RecipeList_{today_date}.txt"
    file_path = os.path.join(directory, file_name)
    with open(file_path, "w") as file:
        file.write("Shopping List:\n")
        for category, items in shopping_list.items():
            file.write(category + ":\n")
            for item in items:
                file.write("- " + item + "\n")

        # Write selected recipes to the file.
        file.write("\nSelected Recipes:\n")
        for recipe_name in selected_recipes:
            file.write("- " + recipe_name + "\n")

        # Write selected recipe links to the file.
        file.write("\nSelected Recipe Links:\n")
        for recipe_name in selected_recipes:
            recipe_data = recipes.get(recipe_name)
            if recipe_data:
                recipe_url = recipe_data.get("url")
                if recipe_url:
                    file.write(f"- [{recipe_name}]({recipe_url})\n")

    # Open the generated .txt file with the default text editor.
    try:
        subprocess.Popen(["open", file_path])
    except subprocess.CalledProcessError:
        print("Unable to open the file automatically. Please open it manually.")

# Specify the directory for saving the shopping list.
output_directory = r"/Users/israelgolden/Documents/PythonProjects/RecipeProgram/Ingredient_txt_files"

# Main program loop
selected_recipes = []

while True:
    print("Available recipes:")
    for recipe_name in recipes.keys():
        print("- " + recipe_name)

    recipe_choice = input("Enter a recipe name (or 'done' to finish): ").strip()

    if recipe_choice.lower() == "done":
        break

    add_recipe_to_shopping_list(recipe_choice)
    selected_recipes.append(recipe_choice)

# Display the final shopping list and save the selected recipe links to a file with a timestamp.
display_shopping_list(selected_recipes)
save_selected_recipes_to_file(output_directory, selected_recipes)