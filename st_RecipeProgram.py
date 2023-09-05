import streamlit as st
import pandas as pd
from collections import defaultdict

# Title and description
st.title("Shopping List Generator")
st.write("Select recipes and generate a shopping list organized by category.")

# Sample recipe data (replace with your actual data)
recipes = {
    "Buttermilk Green Goddess Slaw": {
        "ingredients": [
            {"ingredient": "avocado", "unit": "null", "quantity": 1, "category": "Produce"},
            {"ingredient": "buttermilk", "unit": "cup", "quantity": 0.75, "category": "Dairy"},
            {"ingredient": "lemon", "unit": "null", "quantity": 1, "category": "Produce"},
        ],
        "url": "https://cooking.nytimes.com/recipes/1023266-buttermilk-green-goddess-slaw?action=click&module=Collection%20Page%20Recipe%20Card&region=Sam%20Sifton%E2%80%99s%20Suggestions&pgType=collection&rank=5",
        "Type": "Side",
        "Servings": 6,
        "Kcal/Serving": 149,
        "Contributor": "Israel Golden"
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
        "Kcal/Serving": 177,
        "Contributor": "Israel Golden"
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
        "Kcal/Serving": 495,
        "Contributor": "Israel Golden"
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
            "Kcal/Serving": 311,
            "Contributor": "Israel Golden"
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
        "Kcal/Serving": 300,
        "Contributor": "Israel Golden"
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
        "Kcal/Serving": 320,
        "Contributor": "Israel Golden"
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
        "Kcal/Serving": 364,
        "Contributor": "Israel Golden"
    }, 

}

# Initialize the shopping list as a defaultdict to sum quantities of shared ingredients
shopping_list = defaultdict(float)

# Create a multi-select dropdown to select recipes
selected_recipes = st.multiselect("Select Recipes:", list(recipes.keys()))

# Function to format quantity
def format_quantity(quantity, unit):
    if unit == "null":
        return str(int(quantity))
    elif quantity.is_integer():
        return str(int(quantity)) + " " + unit
    else:
        return "{:.2f}".format(quantity) + " " + unit

# Function to generate the shopping list
def generate_shopping_list(selected_recipes, recipes):
    shopping_list = defaultdict(float)
    for recipe_name in selected_recipes:
        recipe = recipes[recipe_name]
        ingredients = recipe["ingredients"]
        for ingredient_data in ingredients:
            ingredient = ingredient_data["ingredient"]
            unit = ingredient_data["unit"]
            quantity = ingredient_data["quantity"]
            category = ingredient_data["category"]

            # Combine quantities for shared ingredients
            shopping_list[(category, ingredient, unit)] += quantity

    return shopping_list

if st.button("Generate Shopping List"):
    shopping_list = generate_shopping_list(selected_recipes, recipes)

    # Display shopping list organized by category
    categories = set(category for (category, _, _) in shopping_list.keys())
    for category in categories:
        st.subheader(f"{category}:")

        for (cat, ingredient, unit), total_quantity in shopping_list.items():
            if category == cat:
                formatted_quantity = format_quantity(total_quantity, unit)
                st.write(f"- {formatted_quantity} {ingredient}")

# Download shopping list as a .txt file
if shopping_list:
    txt_data = "\n\n".join([f"{category}:\n" + "\n".join([f"- {format_quantity(quantity, unit)} {ingredient}" for (cat, ingredient, unit), quantity in shopping_list.items() if cat == category]) for category in categories])
    st.subheader("Download Shopping List")
    st.text_area("Shopping List Text", txt_data)
    st.download_button("Download Shopping List (.txt)", txt_data, key="download_btn")

# Create a DataFrame with all recipes from the dictionary
all_recipes_info = {
    "Recipe Name": list(recipes.keys()),
    "Number of Servings": [recipes[recipe]["Servings"] for recipe in recipes],
    "Kcal per Serving": [recipes[recipe]["Kcal/Serving"] for recipe in recipes],
    "Side or Main": [recipes[recipe]["Type"] for recipe in recipes],
    "Contributor": [recipes[recipe]["Contributor"] for recipe in recipes],
    "Link": [recipes[recipe]["url"] for recipe in recipes],
}

all_recipes_df = pd.DataFrame(all_recipes_info)


# Display the DataFrame
st.subheader("Recipe Data Frame:")
st.write("Apply filters to tailor your recipe search.")
# st.dataframe(all_recipes_df)

# Create a layout with three columns for filters
col1, col2, col3 = st.columns(3)

# Filter Recipes by Type
with col1:
    selected_type = st.selectbox("Select Recipe Type:", ["All"] + list(set(all_recipes_df["Side or Main"])))
    if selected_type != "All":
        all_recipes_df = all_recipes_df[all_recipes_df["Side or Main"] == selected_type]

# Filter Recipes by Maximum Kcal per Serving
with col2:
    max_kcal = st.slider("Maximum Kcal per Serving:", 0, max(all_recipes_df["Kcal per Serving"]), max(all_recipes_df["Kcal per Serving"]))
    all_recipes_df = all_recipes_df[all_recipes_df["Kcal per Serving"] <= max_kcal]

# Filter Recipes by Contributor
with col3:
    selected_contributor = st.selectbox("Select Contributor:", ["All"] + list(set(all_recipes_df["Contributor"])))
    if selected_contributor != "All":
        all_recipes_df = all_recipes_df[all_recipes_df["Contributor"] == selected_contributor]

# Display the filtered DataFrame
st.dataframe(all_recipes_df)
