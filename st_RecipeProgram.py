import streamlit as st
import pandas as pd
from collections import defaultdict
from io import BytesIO
from datetime import datetime

# Let's get rid of the "Made with Streamlit" at the bottom of the page
st.markdown("""
<style>
.css-cio0dv.ea3mdgi1,
.css-fblp2m.ex0cdmw0
{
            visibility: hidden;
}            
</style>
""", unsafe_allow_html= True
)

# Title and description
st.title("Shopping List Generator")
st.write("Select recipes and generate a shopping list organized by category.")

# Recipe Data
recipes = {
    "Blackened Fish with Quick Grits": {
        "ingredients": [
            {"ingredient": "sweet paprika", "unit": "tbsp", "quantity": 2, "category": "Spices & Condiments"},
            {"ingredient": "dried thyme", "unit": "tsp", "quantity": 2.25, "category": "Spices & Condiments"},
            {"ingredient": "dried oregano", "unit": "tsp", "quantity": 2.25, "category": "Spices & Condiments"},
            {"ingredient": "garlic powder", "unit": "tsp", "quantity": 1.5, "category": "Spices & Condiments"},
            {"ingredient": "ground cayenne", "unit": "tsp", "quantity": 1.5, "category": "Spices & Condiments"},
            {"ingredient": "skinless white fish fillets", "unit": "oz", "quantity": 24, "category": "Fish & Seafood"},
            {"ingredient": "olive oil", "unit": "tbsp", "quantity": 1, "category": "Spices & Condiments"},
            {"ingredient": "unsalted butter", "unit": "tbsp", "quantity": 3, "category": "Dairy"},
            {"ingredient": "scallions", "unit": "null", "quantity": 5, "category": "Produce"},
            {"ingredient": "lemon", "unit": "null", "quantity": 1, "category": "Produce"},
            {"ingredient": "chicken stock", "unit": "cup", "quantity": 3.5, "category": "Soups, Sauces, and Gravies"},
            {"ingredient": "quick-cooking grits", "unit": "cup", "quantity": 1, "category": "Pasta, Rice & Cereal"},
            {"ingredient": "whole milk", "unit": "cup", "quantity": 0.5, "category": "Dairy"},
            {"ingredient": "shredded cheddar", "unit": "cup", "quantity": 1, "category": "Dairy"},
        ],
        "url": "https://cooking.nytimes.com/recipes/1022544-blackened-fish-with-quick-grits",
        "Type": "Main",
        "Servings": 4,
        "Kcal/Serving": 538,
        "Contributor": "Israel Golden",
        "Diet": "Omnivorous"
    },
    "Broccoli Cheddar Soup": {
        "ingredients": [
            {"ingredient": "unsalted butter", "unit": "tbsp", "quantity": 6, "category": "Dairy"},
            {"ingredient": "large yellow onion", "unit": "null", "quantity": 1, "category": "Produce"},
            {"ingredient": "garlic", "unit": "cloves", "quantity": 2, "category": "Produce"},
            {"ingredient": "broccoli", "unit": "pound", "quantity": 2, "category": "Produce"},
            {"ingredient": "all-purpose flour", "unit": "cup", "quantity": 0.25, "category": "Baking"},
            {"ingredient": "chicken stock", "unit": "cup", "quantity": 3, "category": "Soups, Sauces, and Gravies"},
            {"ingredient": "half-and-half", "unit": "cup", "quantity": 2, "category": "Dairy"},
            {"ingredient": "shredded cheddar", "unit": "oz", "quantity": 8, "category": "Dairy"},
            {"ingredient": "nutmeg", "unit": "tsp", "quantity": 0.25, "category": "Condiments & Spices"}
        ],
        "url": "https://cooking.nytimes.com/recipes/1019106-broccoli-and-cheddar-soup",
        "Type": "Main",
        "Servings": 4,
        "Kcal/Serving": 665,
        "Contributor": "Irsael Golden",
        "Diet": "Vegetarian"
    },
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
        "Contributor": "Israel Golden",
        "Diet": "Vegetarian"
    },
    "Cheesy White Bean Tomato Bake": {
        "ingredients": [
            {"ingredient": "olive oil", "unit": "cup", "quantity": 0.25, "category": "Condiments & Spices"},
            {"ingredient": "garlic", "unit": "cloves", "quantity": 3, "category": "Produce"},
            {"ingredient": "tomato paste", "unit": "tbsp", "quantity": 3, "category": "Canned Goods"},
            {"ingredient": "white beans", "unit": "can", "quantity": 2, "category": "Canned Goods"},
            {"ingredient": "shredded mozzarella", "unit": "oz", "quantity": 16, "category": "Dairy"},
        ],
        "url": "https://cooking.nytimes.com/recipes/1019681-cheesy-white-bean-tomato-bake",
        "Type": "Main",
        "Servings": 4,
        "Kcal/Serving": 375,
        "Contributor": "Irsael Golden",
        "Diet": "Vegetarian"
    },
    "Chicken Salad with Walnuts and Grapes": {
        "ingredients": [
            {"ingredient": "mayonnaise", "unit": "cup", "quantity": 0.5, "category": "Condiments & Spices"},
            {"ingredient": "lemon", "unit": "null", "quantity": 1, "category": "Produce"},
            {"ingredient": "chives", "unit": "tsp", "quantity": 1.5, "category": "Produce"},
            {"ingredient": "Italian parsley", "unit": "tsp", "quantity": 1.5, "category": "Produce"},
            {"ingredient": "fresh tarragon", "unit": "tbsp", "quantity": 1, "category": "Produce"},
            {"ingredient": "roast chicken", "unit": "pound", "quantity": 3, "category": "Protein"},
            {"ingredient": "red onion", "unit": "null", "quantity": 1, "category": "Produce"},
            {"ingredient": "celery", "unit": "cup", "quantity": 0.5, "category": "Produce"},
            {"ingredient": "red grapes", "unit": "cup", "quantity": 1, "category": "Produce"},
            {"ingredient": "walnuts", "unit": "cup", "quantity": 0.3, "category": "Snacks"},
        ],
        "url": "https://cooking.nytimes.com/recipes/12107-chicken-salad-with-walnuts-and-grapes",
        "Type": "Main",
        "Servings": 4,
        "Kcal/Serving": 807,
        "Contributor": "Irsael Golden",
        "Diet": "Omnivorous"
    },
    "Chicken Thighs with Sour Cherries and Cucumber Yogurt": {
        "ingredients": [
            {"ingredient": "boneless, skinless chicken thighs", "unit": "pound", "quantity": 2.25, "category": "Protein"},
            {"ingredient": "large red onion", "unit": "null", "quantity": 1, "category": "Produce"},
            {"ingredient": "fresh tarragon", "unit": "tbsp", "quantity": 2, "category": "Produce"},
            {"ingredient": "olive oil", "unit": "tbsp", "quantity": 2.5, "category": "Condiments & Spices"},
            {"ingredient": "rice vinegar", "unit": "cup", "quantity": 0.3, "category": "Condiments & Spices"},
            {"ingredient": "granulated sugar", "unit": "tbsp", "quantity": 3, "category": "Baking"},
            {"ingredient": "bay leaf", "unit": "null", "quantity": 1, "category": "Condiments & Spices"},
            {"ingredient": "Persian cucumbers", "unit": "cup", "quantity": 2, "category": "Produce"},
            {"ingredient": "sour cherries", "unit": "cup", "quantity": 2, "category": "Canned Goods"},
            {"ingredient": "Greek yogurt", "unit": "cup", "quantity": 1, "category": "Dairy"},
        ],
        "url": "https://cooking.nytimes.com/recipes/1023314-chicken-thighs-with-sour-cherries-and-cucumber-yogurt",
        "Type": "Main",
        "Servings": 4,
        "Kcal/Serving": 593,
        "Contributor": "Irsael Golden",
        "Diet": "Omnivorous"
    },
    "Chicken Zucchini Meatballs with Feta": {
        "ingredients": [
            {"ingredient": "zucchini", "unit": "null", "quantity": 3, "category": "Produce"},
            {"ingredient": "shallots", "unit": "null", "quantity": 1, "category": "Produce"},
            {"ingredient": "panko bread crumbs", "unit": "cup", "quantity": 0.5, "category": "Pasta, Rice & Cereal"},
            {"ingredient": "ground cumin", "unit": "tsp", "quantity": 1.5, "category": "Condiments & Spices"},
            {"ingredient": "ground chicken", "unit": "pound", "quantity": 1, "category": "Protein"},
            {"ingredient": "mint, basil, parsley or dill", "unit": "tbsp", "quantity": 2, "category": "Produce"},
            {"ingredient": "lemon", "unit": "null", "quantity": 1, "category": "Produce"},
            {"ingredient": "feta", "unit": "oz", "quantity": 4, "category": "Dairy"},
        ],
        "url": "https://cooking.nytimes.com/recipes/1021328-chicken-zucchini-meatballs-with-feta",
        "Type": "Main",
        "Servings": 4,
        "Kcal/Serving": 468,
        "Contributor": "Irsael Golden",
        "Diet": "Omnivorous"
    },
    "Creamy White Beans with Herb Oil": {
        "ingredients": [
            {"ingredient": "cilantro", "unit": "bunch", "quantity": 1, "category": "Produce"},
            {"ingredient": "basil", "unit": "leaves", "quantity": 20, "category": "Produce"},
            {"ingredient": "olive oil", "unit": "cup", "quantity": 0.5, "category": "Condiments & Spices"},
            {"ingredient": "lemon", "unit": "null", "quantity": 1, "category": "Produce"},
            {"ingredient": "olive oil", "unit": "tbsp", "quantity": 2, "category": "Condiments & Spices"},
            {"ingredient": "garlic", "unit": "cloves", "quantity": 2, "category": "Produce"},
            {"ingredient": "white beans", "unit": "can", "quantity": 2, "category": "Canned Goods"},
            {"ingredient": "chicken stock", "unit": "cup", "quantity": 0.5, "category": "Soups, Sauces, and Gravies"},
        ],
        "url": "https://cooking.nytimes.com/recipes/1019385-creamy-white-beans-with-herb-oil",
        "Type": "Main",
        "Servings": 4,
        "Kcal/Serving": 457,
        "Contributor": "Irsael Golden",
        "Diet": "Vegetarian"
    },
    "Crispy Gnocchi with Burst Tomatoes and Mozzarella": {
        "ingredients": [
            {"ingredient": "olive oil", "unit": "tbsp", "quantity": 2, "category": "Condiments & Spices"},
            {"ingredient": "shelf-stable potato gnocchi", "unit": "oz", "quantity": 24, "category": "Pasta, Rice & Cereal"},
            {"ingredient": "unsalted butter", "unit": "cup", "quantity": 0.25, "category": "Dairy"},
            {"ingredient": "garlic", "unit": "cloves", "quantity": 4, "category": "Produce"},
            {"ingredient": "red-pepper flakes", "unit": "tsp", "quantity": 0.25, "category": "Condiments & Spices"},
            {"ingredient": "cherry tomatoes", "unit": "pint", "quantity": 2, "category": "Produce"},
            {"ingredient": "basil", "unit": "leaves", "quantity": 10, "category": "Produce"},
            {"ingredient": "fresh mozzarella", "unit": "oz", "quantity": 8, "category": "Dairy"},
        ],
        "url": "https://cooking.nytimes.com/recipes/1022024-crispy-gnocchi-with-burst-tomatoes-and-mozzarella",
        "Type": "Main",
        "Servings": 4,
        "Kcal/Serving": 510,
        "Contributor": "Irsael Golden",
        "Diet": "Vegetarian"
    },
    "Garlic Chicken with Guasaca Sauce": {
        "ingredients": [
            {"ingredient": "olive oil", "unit": "cup", "quantity": 0.5, "category": "Condiments & Spices"},
            {"ingredient": "garlic", "unit": "cloves", "quantity": 3, "category": "Produce"},
            {"ingredient": "carrot", "unit": "pound", "quantity": 1.5, "category": "Produce"},
            {"ingredient": "bone-in, skin-on chicken thighs", "unit": "pound", "quantity": 3, "category": "Protein"},
            {"ingredient": "avocado", "unit": "null", "quantity": 1, "category": "Produce"},
            {"ingredient": "jalapeño", "unit": "null", "quantity": 1, "category": "Produce"},
            {"ingredient": "rice vinegar", "unit": "tbsp", "quantity": 2, "category": "Condiments & Spices"},
            {"ingredient": "lime", "unit": "null", "quantity": 1, "category": "Produce"},
            {"ingredient": "Italian parsley", "unit": "cup", "quantity": 1, "category": "Produce"},
            {"ingredient": "cilantro", "unit": "cup", "quantity": 1, "category": "Produce"},
        ],
        "url": "https://cooking.nytimes.com/recipes/1022128-garlic-chicken-with-guasacaca-sauce",
        "Type": "Main",
        "Servings": 4,
        "Kcal/Serving": 816,
        "Contributor": "Irsael Golden",
        "Diet": "Omnivorous"
    },
    "Garlicky Chicken Thighs With Scallion and Lime": {
        "ingredients": [
            {"ingredient": "bone-in, skin-on chicken thighs", "unit": "pound", "quantity": 1.5, "category": "Protein"},
            {"ingredient": "canola oil", "unit": "tbsp", "quantity": 1, "category": "Condiments & Spices"},
            {"ingredient": "scallions", "unit": "null", "quantity": 5, "category": "Produce"},
            {"ingredient": "garlic", "unit": "head", "quantity": 1, "category": "Produce"},
            {"ingredient": "garlic", "unit": "cloves", "quantity": 2, "category": "Produce"},
            {"ingredient": "lime", "unit": "null", "quantity": 1, "category": "Produce"},
            {"ingredient": "soy sauce", "unit": "tbsp", "quantity": 1, "category": "Condiments & Spices"},
        ],
        "url": "https://cooking.nytimes.com/recipes/1018911-garlicky-chicken-thighs-with-scallion-and-lime",
        "Type": "Main",
        "Servings": 4,
        "Kcal/Serving": 370,
        "Contributor": "Irsael Golden",
        "Diet": "Omnivorous"
    },
    "Ginger Dill Salmon": {
        "ingredients": [
            {"ingredient": "salmon fillet", "unit": "pound", "quantity": 1.5, "category": "Fish & Seafood"},
            {"ingredient": "fresh dill", "unit": "tbsp", "quantity": 6, "category": "Produce"},
            {"ingredient": "ginger", "unit": "tbsp", "quantity": 2, "category": "Produce"},
            {"ingredient": "olive oil", "unit": "tbsp", "quantity": 2, "category": "Condiments & Spices"},
            {"ingredient": "grapefruit", "unit": "null", "quantity": 1, "category": "Produce"},
            {"ingredient": "orange", "unit": "null", "quantity": 2, "category": "Produce"},
            {"ingredient": "radishes", "unit": "null", "quantity": 6, "category": "Produce"},
            {"ingredient": "avocado", "unit": "null", "quantity": 1, "category": "Produce"},
        ],
        "url": "https://cooking.nytimes.com/recipes/1021938-ginger-dill-salmon",
        "Type": "Main",
        "Servings": 4,
        "Kcal/Serving": 570,
        "Contributor": "Irsael Golden",
        "Diet": "Omnivorous"
    },
    "Lemon Dill Meatball with Orzo": {
        "ingredients": [
            {"ingredient": "fresh dill", "unit": "oz", "quantity": 3, "category": "Produce"},
            {"ingredient": "Greek yogurt", "unit": "cup", "quantity": 1, "category": "Dairy"},
            {"ingredient": "lemon", "unit": "null", "quantity": 1, "category": "Produce"},
            {"ingredient": "ground chicken", "unit": "pound", "quantity": 1, "category": "Protein"},
            {"ingredient": "fennel seeds", "unit": "tsp", "quantity": 1, "category": "Condiments & Spices"},
            {"ingredient": "unsalted butter", "unit": "tbsp", "quantity": 2, "category": "Dairy"},
            {"ingredient": "orzo", "unit": "cup", "quantity": 1, "category": "Pasta, Rice & Cereal"},
            {"ingredient": "anchovy", "unit": "fillets", "quantity": 3, "category": "Canned Goods"},
            {"ingredient": "garlic", "unit": "cloves", "quantity": 1, "category": "Produce"},
            {"ingredient": "spinach", "unit": "cups", "quantity": 4, "category": "Produce"},
        ],
        "url": "https://cooking.nytimes.com/recipes/1024124-lemon-dill-meatballs-with-orzo",
        "Type": "Main",
        "Servings": 4,
        "Kcal/Serving": 387,
        "Contributor": "Irsael Golden",
        "Diet": "Omnivorous"
    },
    "Mojo Chicken with Pineapple": {
        "ingredients": [
            {"ingredient": "boneless, skinless chicken thighs", "unit": "pound", "quantity": 2, "category": "Protein"},
            {"ingredient": "pineapple", "unit": "cup", "quantity": 3, "category": "Produce"},
            {"ingredient": "orange", "unit": "null", "quantity": 1, "category": "Produce"},
            {"ingredient": "garlic", "unit": "cloves", "quantity": 1, "category": "Produce"},
            {"ingredient": "jalapeño", "unit": "null", "quantity": 1, "category": "Produce"},
            {"ingredient": "cilantro", "unit": "bunch", "quantity": 1, "category": "Produce"},
            {"ingredient": "lime", "unit": "null", "quantity": 2, "category": "Produce"},
            {"ingredient": "dried oregano", "unit": "tsp", "quantity": 1, "category": "Condiments & Spices"},
            {"ingredient": "ground cumin", "unit": "tsp", "quantity": 0.5, "category": "Condiments & Spices"},
        ],
        "url": "https://cooking.nytimes.com/recipes/1020758-mojo-chicken-with-pineapple",
        "Type": "Main",
        "Servings": 4,
        "Kcal/Serving": 496,
        "Contributor": "Irsael Golden",
        "Diet": "Omnivorous"
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
            {"ingredient": "Italian parsley", "unit": "cup", "quantity": 1, "category": "Produce"},
            {"ingredient": "russet potatoes", "unit": "pound", "quantity": 3, "category": "Produce"},
            {"ingredient": "whole milk", "unit": "cup", "quantity": 1.5, "category": "Dairy"},
            {"ingredient": "unsalted butter", "unit": "tbsp", "quantity": 4, "category": "Dairy"},
        ],
        "url": "https://cooking.nytimes.com/recipes/1022724-mushroom-stroganoff",
        "Type": "Main",
        "Servings": 4,
        "Kcal/Serving": 495,
        "Contributor": "Israel Golden",
        "Diet": "Vegetarian"
    },
    "Oklahoma Onion Burgers": {
        "ingredients": [
            {"ingredient": "ground beef", "unit": "pound", "quantity": 1, "category": "Protein"},
            {"ingredient": "large yellow onion", "unit": "null", "quantity": 1, "category": "Produce"},
            {"ingredient": "American cheese", "unit": "slices", "quantity": 4, "category": "Dairy"},
            {"ingredient": "hamburger buns", "unit": "null", "quantity": 4, "category": "Bread & Bakery"},
            {"ingredient": "dill pickle chips", "unit": "null", "quantity": 12, "category": "Canned Goods"},
            {"ingredient": "ketchup", "unit": "tbsp", "quantity": 4, "category": "Condiments & Spices"},
            {"ingredient": "mayonnaise", "unit": "tbsp", "quantity": 4, "category": "Condiments & Spices"},
        ],
        "url": "https://cooking.nytimes.com/recipes/1023331-oklahoma-onion-burgers",
        "Type": "Main",
        "Servings": 4,
        "Kcal/Serving": 626,
        "Contributor": "Irsael Golden",
        "Diet": "Omnivorous"
    },
    "Orecchiette with Corn, Jalapeño, Feta and Basil": {
        "ingredients": [
            {"ingredient": "orecchiette", "unit": "pound", "quantity": 1, "category": "Pasta, Rice & Cereal"},
            {"ingredient": "unsalted butter", "unit": "tbsp", "quantity": 4, "category": "Dairy"},
            {"ingredient": "jalapeño", "unit": "null", "quantity": 1, "category": "Produce"},
            {"ingredient": "corn", "unit": "cup", "quantity": 4, "category": "Canned Goods"},
            {"ingredient": "feta", "unit": "oz", "quantity": 8, "category": "Dairy"},
            {"ingredient": "basil", "unit": "leaves", "quantity": 20, "category": "Produce"},

        ],
        "url": "https://cooking.nytimes.com/recipes/1019464-orecchiette-with-corn-jalapeno-feta-and-basil",
        "Type": "Main",
        "Servings": 4,
        "Kcal/Serving": 578,
        "Contributor": "Irsael Golden",
        "Diet": "Vegetarian"
    },
    "Peach and Molasses Chicken": {
        "ingredients": [
            {"ingredient": "peach jam", "unit": "cup", "quantity": 0.5, "category": "Canned Goods"},
            {"ingredient": "unsulfured molasses", "unit": "cup", "quantity": 0.25, "category": "Condiments & Spices"},
            {"ingredient": "apple cider vinegar", "unit": "tbsp", "quantity": 1, "category": "Condiments & Spices"},
            {"ingredient": "tomato paste", "unit": "tbsp", "quantity": 2, "category": "Canned Goods"},
            {"ingredient": "soy sauce", "unit": "tbsp", "quantity": 1, "category": "Condiments & Spices"},
            {"ingredient": "coriander seeds", "unit": "tbsp", "quantity": 2, "category": "Condiments & Spices"},
            {"ingredient": "ground mustard", "unit": "tbsp", "quantity": 1, "category": "Condiments & Spices"},
            {"ingredient": "bone-in, skin-on chicken thighs", "unit": "pound", "quantity": 4, "category": "Protein"},
            {"ingredient": "peanut oil", "unit": "tbsp", "quantity": 1.5, "category": "Condiments & Spices"},

        ],
        "url": "https://cooking.nytimes.com/recipes/1023220-peach-and-molasses-chicken",
        "Type": "Main",
        "Servings": 6,
        "Kcal/Serving": 644,
        "Contributor": "Irsael Golden",
        "Diet": "Omnivorous"
    },
    "Rice Noodles With Spicy Pork and Herbs": {
        "ingredients": [
            {"ingredient": "round rice noodles", "unit": "pound", "quantity": 1, "category": "Pasta, Rice & Cereal"},
            {"ingredient": "rice vinegar", "unit": "tbsp", "quantity": 2, "category": "Condiments & Spices"},
            {"ingredient": "black vinegar", "unit": "tbsp", "quantity": 1, "category": "Condiments & Spices"},
            {"ingredient": "chile oil", "unit": "tbsp", "quantity": 1, "category": "Condiments & Spices"},
            {"ingredient": "granulated sugar", "unit": "tsp", "quantity": 1, "category": "Baking"},
            {"ingredient": "canola oil", "unit": "tbsp", "quantity": 1, "category": "Condiments & Spices"},
            {"ingredient": "pork", "unit": "pound", "quantity": 0.5, "category": "Protein"},
            {"ingredient": "garlic", "unit": "cloves", "quantity": 2, "category": "Produce"},
            {"ingredient": "ginger", "unit": "tbsp", "quantity": 1, "category": "Produce"},
            {"ingredient": "scallions", "unit": "null", "quantity": 2, "category": "Produce"},
            {"ingredient": "yacai - Sichuan preserved vegetables", "unit": "tbsp", "quantity": 1, "category": "Canned Goods"},
            {"ingredient": "basil", "unit": "leaves", "quantity": 8, "category": "Produce"},
            {"ingredient": "salted, roasted peanuts", "unit": "cup", "quantity": 0.25, "category": "Snacks"},
            {"ingredient": "breakfast radish", "unit": "null", "quantity": 4, "category": "Produce"},

        ],
        "url": "https://cooking.nytimes.com/recipes/1018852-rice-noodles-with-spicy-pork-and-herbs",
        "Type": "Main",
        "Servings": 4,
        "Kcal/Serving": 311,
        "Contributor": "Israel Golden",
        "Diet": "Omnivorous"
    },
    "Rigatoni alla Zozzona": {
        "ingredients": [
            {"ingredient": "rigatoni", "unit": "pound", "quantity": 1, "category": "Pasta, Rice & Cereal"},
            {"ingredient": "olive oil", "unit": "tbsp", "quantity": 2, "category": "Condiments & Spices"},
            {"ingredient": "bacon", "unit": "oz", "quantity": 4, "category": "Protein"},
            {"ingredient": "small yellow onion", "unit": "null", "quantity": 1, "category": "Produce"},
            {"ingredient": "hot Italian sausages", "unit": "pound", "quantity": 1, "category": "Protein"},
            {"ingredient": "tomato paste", "unit": "tbsp", "quantity": 2, "category": "Canned Goods"},
            {"ingredient": "cherry tomatoes", "unit": "cup", "quantity": 3, "category": "Produce"},
            {"ingredient": "red wine", "unit": "cup", "quantity": 1, "category": "Beverages"},
            {"ingredient": "eggs", "unit": "null", "quantity": 4, "category": "Dairy"},
            {"ingredient": "Pecorino Romano", "unit": "cup", "quantity": 0.25, "category": "Dairy"},
        ],
        "url": "https://cooking.nytimes.com/recipes/1023212-rigatoni-alla-zozzona",
        "Type": "Main",
        "Servings": 4,
        "Kcal/Serving": 893,
        "Contributor": "Irsael Golden",
        "Diet": "Omnivorous"
    },
    "Roasted Salmon and Brussels Sprouts with Citrus Soy Sauce": {
        "ingredients": [
            {"ingredient": "brussel sprouts", "unit": "pound", "quantity": 1, "category": "Produce"},
            {"ingredient": "scallions", "unit": "null", "quantity": 5, "category": "Produce"},
            {"ingredient": "jalapeño", "unit": "null", "quantity": 1, "category": "Produce"},
            {"ingredient": "toasted sesame oil", "unit": "tbsp", "quantity": 2, "category": "Condiments & Spices"},
            {"ingredient": "skin-on salmon fillets", "unit": "oz", "quantity": 24, "category": "Fish & Seafood"},
            {"ingredient": "lemon", "unit": "null", "quantity": 1, "category": "Produce"},
            {"ingredient": "rice vinegar", "unit": "tbsp", "quantity": 2, "category": "Condiments & Spices"},
            {"ingredient": "honey", "unit": "tbsp", "quantity": 4, "category": "Condiments & Spices"},
        ],
        "url": "https://cooking.nytimes.com/recipes/1019900-roasted-salmon-and-brussels-sprouts-with-citrus-soy-sauce",
        "Type": "Main",
        "Servings": 4,
        "Kcal/Serving": 487,
        "Contributor": "Irsael Golden",
        "Diet": "Omnivorous"
    },
    "Rotisserie Chicken with Greens Pasta": {
        "ingredients": [
            {"ingredient": "rigatoni", "unit": "pound", "quantity": 1, "category": "Pasta, Rice & Cereal"},
            {"ingredient": "rotisserie chicken", "unit": "null", "quantity": 1, "category": "Protein"},
            {"ingredient": "unsalted butter", "unit": "tbsp", "quantity": 3, "category": "Dairy"},
            {"ingredient": "medium yellow onion", "unit": "null", "quantity": 1, "category": "Produce"},
            {"ingredient": "garlic", "unit": "cloves", "quantity": 5, "category": "Produce"},
            {"ingredient": "Dijon mustard", "unit": "tsp", "quantity": 2, "category": "Condiments & Spices"},
            {"ingredient": "chicken stock", "unit": "cup", "quantity": 1, "category": "Soups, Sauces, and Gravies"},
            {"ingredient": "heavy cream", "unit": "cup", "quantity": 0.5, "category": "Dairy"},
            {"ingredient": "spinach", "unit": "oz", "quantity": 10, "category": "Produce"},
            {"ingredient": "lemon", "unit": "null", "quantity": 1, "category": "Produce"},
            {"ingredient": "parmesan", "unit": "cup", "quantity": 1, "category": "Dairy"},

        ],
        "url": "https://cooking.nytimes.com/recipes/1023870-rotisserie-chicken-and-greens-pasta",
        "Type": "Main",
        "Servings": 4,
        "Kcal/Serving": 696,
        "Contributor": "Irsael Golden",
        "Diet": "Omnivorous"
    },
    "Salmon and Couscous Salad with Cucumber Feta Dressing": {
        "ingredients": [
            {"ingredient": "salmon fillet", "unit": "oz", "quantity": 18, "category": "Fish & Seafood"},
            {"ingredient": "olive oil", "unit": "tbsp", "quantity": 2, "category": "Condiments & Spices"},
            {"ingredient": "ground cumin", "unit": "tsp", "quantity": 1, "category": "Condiments & Spices"},
            {"ingredient": "ground tumeric", "unit": "tsp", "quantity": 0.5, "category": "Condiments & Spices"},
            {"ingredient": "lime", "unit": "null", "quantity": 2, "category": "Produce"},
            {"ingredient": "pearl couscous", "unit": "cup", "quantity": 1.5, "category": "Pasta, Rice & Cereal"},
            {"ingredient": "baby arugula", "unit": "cup", "quantity": 1.5, "category": "Produce"},
            {"ingredient": "Greek yogurt", "unit": "cup", "quantity": 1, "category": "Dairy"},
            {"ingredient": "feta", "unit": "cup", "quantity": 0.5, "category": "Dairy"},
            {"ingredient": "Italian parsley", "unit": "cup", "quantity": 0.25, "category": "Produce"},
            {"ingredient": "mint", "unit": "cup", "quantity": 0.25, "category": "Produce"},
            {"ingredient": "Persian cucumbers", "unit": "null", "quantity": 1, "category": "Produce"},
            {"ingredient": "scallions", "unit": "null", "quantity": 2, "category": "Produce"},

        ],
        "url": "https://cooking.nytimes.com/recipes/1021970-salmon-and-couscous-salad-with-cucumber-feta-dressing",
        "Type": "Main",
        "Servings": 4,
        "Kcal/Serving": 640,
        "Contributor": "Irsael Golden",
        "Diet": "Omnivorous"
    },
    "Sesame Salmon Bowls": {
        "ingredients": [
            {"ingredient": "rice vinegar", "unit": "cup", "quantity": 0.25, "category": "Condiments & Spices"},
            {"ingredient": "granulated sugar", "unit": "tbsp", "quantity": 3, "category": "Baking"},
            {"ingredient": "sushi rice", "unit": "cup", "quantity": 1.5, "category": "Pasta, Rice & Cereal"},
            {"ingredient": "skinless, salmon filet", "unit": "pound", "quantity": 1.5, "category": "Fish & Seafood"},
            {"ingredient": "toasted sesame oil", "unit": "tsp", "quantity": 0.5, "category": "Condiments & Spices"},
            {"ingredient": "soy sauce", "unit": "cup", "quantity": 0.25, "category": "Condiments & Spices"},
            {"ingredient": "distilled white vinegar", "unit": "tbsp", "quantity": 3, "category": "Condiments & Spices"},
            {"ingredient": "canola oil", "unit": "tbsp", "quantity": 2, "category": "Condiments & Spices"},
            {"ingredient": "scallions", "unit": "null", "quantity": 2, "category": "Produce"},
            {"ingredient": "ginger", "unit": "tbsp", "quantity": 2, "category": "Produce"},
            {"ingredient": "Persian cucumbers", "unit": "null", "quantity": 3, "category": "Produce"},
            {"ingredient": "green coleslaw mix", "unit": "oz", "quantity": 8, "category": "Produce"},
            {"ingredient": "avocado", "unit": "null", "quantity": 1, "category": "Produce"},
            {"ingredient": "nori", "unit": "sheets", "quantity": 4, "category": "Snacks"},
        ],
        "url": "https://cooking.nytimes.com/recipes/1022255-sesame-salmon-bowls",
        "Type": "Main",
        "Servings": 4,
        "Kcal/Serving": 478,
        "Contributor": "Irsael Golden",
        "Diet": "Omnivorous"
    },
    "Shakshuka with Feta": {
        "ingredients": [
            {"ingredient": "olive oil", "unit": "tbsp", "quantity": 3, "category": "Condiments & Spices"},
            {"ingredient": "large onion", "unit": "null", "quantity": 1, "category": "Produce"},
            {"ingredient": "red bell pepper", "unit": "null", "quantity": 1, "category": "Produce"},
            {"ingredient": "garlic", "unit": "cloves", "quantity": 3, "category": "Produce"},
            {"ingredient": "ground cumin", "unit": "tsp", "quantity": 1, "category": "Condiments & Spices"},
            {"ingredient": "sweet paprika", "unit": "tsp", "quantity": 1, "category": "Condiments & Spices"},
            {"ingredient": "ground cayenne", "unit": "tsp", "quantity": 0.2, "category": "Condiments & Spices"},
            {"ingredient": "whole plum tomatoes", "unit": "oz", "quantity": 28, "category": "Canned Goods"},
            {"ingredient": "feta", "unit": "oz", "quantity": 5, "category": "Dairy"},
            {"ingredient": "eggs", "unit": "null", "quantity": 6, "category": "Dairy"},
            {"ingredient": "cilantro", "unit": "bunch", "quantity": 1, "category": "Produce"},
            {"ingredient": "Hot sauce", "unit": "bottle", "quantity": 1, "category": "Condiments & Spices"},
        ],
        "url": "https://cooking.nytimes.com/recipes/1014721-shakshuka-with-feta",
        "Type": "Main",
        "Servings": 4,
        "Kcal/Serving": 383,
        "Contributor": "Irsael Golden",
        "Diet": "Vegetarian"
    },
    "Sheet-Pan Mushroom Parmagiana": {
        "ingredients": [
            {"ingredient": "cherry tomatoes", "unit": "oz", "quantity": 10, "category": "Produce"},
            {"ingredient": "garlic", "unit": "cloves", "quantity": 2, "category": "Produce"},
            {"ingredient": "olive oil", "unit": "tbsp", "quantity": 4, "category": "Condiments & Spices"},
            {"ingredient": "portobello mushrooms", "unit": "null", "quantity": 8, "category": "Produce"},
            {"ingredient": "marinara sauce", "unit": "cup", "quantity": 3, "category": "Canned Goods"},
            {"ingredient": "shredded mozzarella", "unit": "oz", "quantity": 12, "category": "Dairy"},
            {"ingredient": "panko bread crumbs", "unit": "cup", "quantity": 1, "category": "Pasta, Rice & Cereal"},
        ],
        "url": "https://cooking.nytimes.com/recipes/1022803-sheet-pan-mushroom-parmigiana",
        "Type": "Main",
        "Servings": 4,
        "Kcal/Serving": 446,
        "Contributor": "Irsael Golden",
        "Diet": "Vegetarian"
    },
    "Sheet-Pan Sausage With Peppers and Tomatoes": {
        "ingredients": [
            {"ingredient": "fresh sausage", "unit": "pound", "quantity": 1, "category": "Protein"},
            {"ingredient": "sweet or mild peppers", "unit": "pound", "quantity": 1, "category": "Produce"},
            {"ingredient": "cherry tomatoes", "unit": "pound", "quantity": 1, "category": "Produce"},
            {"ingredient": "garlic", "unit": "cloves", "quantity": 4, "category": "Produce"},
            {"ingredient": "shallots", "unit": "null", "quantity": 2, "category": "Produce"},
            {"ingredient": "olive oil", "unit": "tbsp", "quantity": 3, "category": "Condiments & Spices"},
        ],
        "url": "https://cooking.nytimes.com/recipes/1020436-sheet-pan-sausage-with-peppers-and-tomatoes",
        "Type": "Main",
        "Servings": 4,
        "Kcal/Serving": 440,
        "Contributor": "Irsael Golden",
        "Diet": "Omnivorous"
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
            {"ingredient": "Italian parsley", "unit": "cup", "quantity": 0.2, "category": "Produce"},
        ],
        "url": "https://cooking.nytimes.com/recipes/1020330-shrimp-scampi-with-orzo",
        "Type": "Main",
        "Servings": 4,
        "Kcal/Serving": 364,
        "Contributor": "Israel Golden",
        "Diet": "Omnivorous",
    }, 
    "Smashed Avocado & Chicken Burgers": {
        "ingredients": [
            {"ingredient": "mayonnaise", "unit": "tbsp", "quantity": 4, "category": "Condiments & Spices"},
            {"ingredient": "soy sauce", "unit": "tsp", "quantity": 1, "category": "Condiments & Spices"},
            {"ingredient": "cilantro", "unit": "bunch", "quantity": 1, "category": "Produce"},
            {"ingredient": "avocado", "unit": "null", "quantity": 1, "category": "Produce"},
            {"ingredient": "ginger", "unit": "tbsp", "quantity": 2, "category": "Produce"},
            {"ingredient": "scallions", "unit": "null", "quantity": 2, "category": "Produce"},
            {"ingredient": "garlic", "unit": "cloves", "quantity": 3, "category": "Produce"},
            {"ingredient": "red-pepper flakes", "unit": "tsp", "quantity": 0.5, "category": "Condiments & Spices"},
            {"ingredient": "ground chicken", "unit": "pound", "quantity": 1, "category": "Protein"},
            {"ingredient": "canola oil", "unit": "tbsp", "quantity": 2, "category": "Condiments & Spices"},
            {"ingredient": "brioche buns", "unit": "null", "quantity": 4, "category": "Bread & Bakery"},
            {"ingredient": "butter lettuce", "unit": "head", "quantity": 1, "category": "Produce"},
            {"ingredient": "jalapeño", "unit": "null", "quantity": 1, "category": "Produce"},

        ],
        "url": "https://cooking.nytimes.com/recipes/1023132-smashed-avocado-chicken-burgers",
        "Type": "Main",
        "Servings": 4,
        "Kcal/Serving": 635,
        "Contributor": "Irsael Golden",
        "Diet": "Omnivorous"
    },
    "Smashed Chicken Burgers with Cheddar and Parsley": {
        "ingredients": [
            {"ingredient": "mayonnaise", "unit": "cup", "quantity": 0.5, "category": "Condiments & Spices"},
            {"ingredient": "Dijon mustard", "unit": "tsp", "quantity": 1, "category": "Condiments & Spices"},
            {"ingredient": "lime", "unit": "null", "quantity": 2, "category": "Produce"},
            {"ingredient": "Italian parsley", "unit": "cup", "quantity": 1.25, "category": "Produce"},
            {"ingredient": "grated cheddar", "unit": "cup", "quantity": 0.3, "category": "Dairy"},
            {"ingredient": "cheddar", "unit": "slices", "quantity": 8, "category": "Dairy"},
            {"ingredient": "shallots", "unit": "null", "quantity": 1, "category": "Produce"},
            {"ingredient": "garlic", "unit": "cloves", "quantity": 3, "category": "Produce"},
            {"ingredient": "ground cumin", "unit": "tsp", "quantity": 1, "category": "Condiments & Spices"},
            {"ingredient": "red-pepper flakes", "unit": "tsp", "quantity": 0.5, "category": "Condiments & Spices"},
            {"ingredient": "ground chicken", "unit": "pound", "quantity": 1, "category": "Protein"},
            {"ingredient": "canola oil", "unit": "tbsp", "quantity": 2, "category": "Condiments & Spices"},
            {"ingredient": "olive oil", "unit": "tbsp", "quantity": 3, "category": "Condiments & Spices"},
            {"ingredient": "butter lettuce", "unit": "head", "quantity": 1, "category": "Produce"},
            {"ingredient": "avocado", "unit": "null", "quantity": 1, "category": "Produce"},
            {"ingredient": "brioche buns", "unit": "null", "quantity": 4, "category": "Bread & Bakery"},
        ],
        "url": "https://cooking.nytimes.com/recipes/1021780-smashed-chicken-burgers-with-cheddar-and-parsley",
        "Type": "Main",
        "Servings": 4,
        "Kcal/Serving": 1122,
        "Contributor": "Irsael Golden",
        "Diet": "Omnivorous"
    },
    "Spicy Honey Chicken with Broccoli": {
        "ingredients": [

            {"ingredient": "olive oil", "unit": "tbsp", "quantity": 2, "category": "Condiments & Spices"},
            {"ingredient": "honey", "unit": "tbsp", "quantity": 1, "category": "Condiments & Spices"},
            {"ingredient": "boneless, skinless chicken thighs", "unit": "pounds", "quantity": 1.5, "category": "Protein"},
            {"ingredient": "pickled jalapeños", "unit": "tbsp", "quantity": 2, "category": "Canned Goods"},
            {"ingredient": "broccoli", "unit": "head", "quantity": 1, "category": "Produce"},
            {"ingredient": "feta", "unit": "cup", "quantity": 0.5, "category": "Dairy"},
        ],
        "url": "https://cooking.nytimes.com/recipes/1024005-spicy-honey-chicken-with-broccoli",
        "Type": "Main",
        "Servings": 4,
        "Kcal/Serving": 440,
        "Contributor": "Irsael Golden",
        "Diet": "Omnivorous"
    },
    "Stone Fruit Caprese": {
        "ingredients": [
            {"ingredient": "stone fruit", "unit": "pound", "quantity": 2, "category": "Produce"},
            {"ingredient": "lemon", "unit": "null", "quantity": 1, "category": "Produce"},
            {"ingredient": "granulated sugar", "unit": "tsp", "quantity": 2, "category": "Baking"},
            {"ingredient": "fresh mozzarella", "unit": "oz", "quantity": 8, "category": "Dairy"},
            {"ingredient": "basil", "unit": "leaves", "quantity": 20, "category": "Produce"},
            {"ingredient": "olive oil", "unit": "tbsp", "quantity": 2, "category": "Condiments & Spices"},
        ],
        "url": "https://cooking.nytimes.com/recipes/1023336-stone-fruit-caprese",
        "Type": "Side",
        "Servings": 4,
        "Kcal/Serving": 300,
        "Contributor": "Israel Golden",
        "Diet": "Vegetarian"
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
            {"ingredient": "chicken stock", "unit": "cup", "quantity": 0.75, "category": "Soups, Sauces, and Gravies"},
            {"ingredient": "canned diced fire-roasted tomatoes", "unit": "oz", "quantity": 14, "category": "Canned Goods"},
            {"ingredient": "white rice", "unit": "cup", "quantity": 1, "category": "Pasta, Rice & Cereal"},
            {"ingredient": "parmesan", "unit": "cup", "quantity": 0.25, "category": "Dairy"},
            {"ingredient": "Italian parsley", "unit": "cup", "quantity": 0.125, "category": "Produce"},
            {"ingredient": "shredded mozzarella", "unit": "cup", "quantity": 1, "category": "Dairy"},
        ],
        "url": "https://cooking.nytimes.com/recipes/1021007-stuffed-peppers",
        "Type": "Main",
        "Servings": 6,
        "Kcal/Serving": 320,
        "Contributor": "Israel Golden",
        "Diet": "Omnivorous"
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
        "Contributor": "Israel Golden",
        "Diet": "Vegetarian"
    },
    "Tuna Melt": {
        "ingredients": [
            {"ingredient": "tuna in water", "unit": "can", "quantity": 3, "category": "Canned Goods"},
            {"ingredient": "mayonnaise", "unit": "cup", "quantity": 0.75, "category": "Condiments & Spices"},
            {"ingredient": "cornichons", "unit": "cup", "quantity": 0.25, "category": "Canned Goods"},
            {"ingredient": "red onion", "unit": "null", "quantity": 1, "category": "Produce"},
            {"ingredient": "lemon", "unit": "null", "quantity": 1, "category": "Produce"},
            {"ingredient": "fresh dill", "unit": "tbsp", "quantity": 1, "category": "Produce"},
            {"ingredient": "whole-grain mustard", "unit": "tsp", "quantity": 2, "category": "Condiments & Spices"},
            {"ingredient": "sourdough bread", "unit": "slices", "quantity": 8, "category": "Bread & Bakery"},
            {"ingredient": "extra-sharp Cheddar", "unit": "slices", "quantity": 8, "category": "Dairy"},
            {"ingredient": "unsalted butter", "unit": "tbsp", "quantity": 4, "category": "Dairy"},
        ],
        "url": "https://cooking.nytimes.com/recipes/1021806-tuna-melt",
        "Type": "Main",
        "Servings": 4,
        "Kcal/Serving": 954,
        "Contributor": "Irsael Golden",
        "Diet": "Omnivorous"
    },
    "Tuna Salad Sandwiches": {
        "ingredients": [
            {"ingredient": "tuna in water", "unit": "can", "quantity": 2, "category": "Canned Goods"},
            {"ingredient": "mayonnaise", "unit": "tbsp", "quantity": 2, "category": "Condiments & Spices"},
            {"ingredient": "dill pickles", "unit": "cup", "quantity": 0.5, "category": "Canned Goods"},
            {"ingredient": "celery stalk", "unit": "null", "quantity": 1, "category": "Produce"},
            {"ingredient": "fresh dill", "unit": "cup", "quantity": 0.25, "category": "Produce"},
            {"ingredient": "Italian parsley", "unit": "cup", "quantity": 0.5, "category": "Produce"},
            {"ingredient": "lemon", "unit": "null", "quantity": 1, "category": "Produce"},
            {"ingredient": "olive oil", "unit": "tbsp", "quantity": 2, "category": "Condiments & Spices"},
            {"ingredient": "ciabatta sandwich rolls", "unit": "null", "quantity": 4, "category": "Bread & Bakery"},
            {"ingredient": "potato chips", "unit": "bag", "quantity": 1, "category": "Snacks"},
        ],
        "url": "https://cooking.nytimes.com/recipes/1022354-tuna-salad-sandwiches",
        "Type": "Main",
        "Servings": 4,
        "Kcal/Serving": 490,
        "Contributor": "Irsael Golden",
        "Diet": "Omnivorous"
    },

    "Vegetarian Tamale Pie": {
        "ingredients": [
            {"ingredient": "white onion", "unit": "null", "quantity": 1, "category": "Produce"},
            {"ingredient": "jalapeño", "unit": "null", "quantity": 2, "category": "Produce"},
            {"ingredient": "poblano or green bell pepper", "unit": "null", "quantity": 1, "category": "Produce"},
            {"ingredient": "olive oil", "unit": "tbsp", "quantity": 2, "category": "Condiments & Spices"},
            {"ingredient": "whole plum or diced tomatoes", "unit": "oz", "quantity": 28, "category": "Canned Goods"},
            {"ingredient": "garlic", "unit": "cloves", "quantity": 3, "category": "Produce"},
            {"ingredient": "chili powder", "unit": "tbsp", "quantity": 2, "category": "Condiments & Spices"},
            {"ingredient": "pinto beans", "unit": "can", "quantity": 1, "category": "Canned Goods"},
            {"ingredient": "dried oregano", "unit": "tsp", "quantity": 2, "category": "Condiments & Spices"},
            {"ingredient": "ground cumin", "unit": "tsp", "quantity": 1.75, "category": "Condiments & Spices"},
            {"ingredient": "pinto beans", "unit": "15 oz can", "quantity": 3, "category": "Canned Goods"},
            {"ingredient": "cilantro", "unit": "bunch", "quantity": 1, "category": "Produce"},
            {"ingredient": "fine cornmeal", "unit": "cup", "quantity": 0.75, "category": "Baking"},
            {"ingredient": "all-purpose flour", "unit": "tbsp", "quantity": 2, "category": "Baking"},
            {"ingredient": "baking powder", "unit": "tsp", "quantity": 1.5, "category": "Baking"},
            {"ingredient": "eggs", "unit": "null", "quantity": 1, "category": "Dairy"},
            {"ingredient": "sour cream", "unit": "cup", "quantity": 0.3, "category": "Dairy"},
            {"ingredient": "unsalted butter", "unit": "cup", "quantity": 0.25, "category": "Dairy"},
            {"ingredient": "honey", "unit": "tsp", "quantity": 2, "category": "Condiments & Spices"},
            {"ingredient": "scallions", "unit": "null", "quantity": 2, "category": "Produce"},
            {"ingredient": "cheddar", "unit": "cup", "quantity": 1, "category": "Dairy"},
        ],
        "url": "https://cooking.nytimes.com/recipes/1023880-vegetarian-tamale-pie",
        "Type": "Main",
        "Servings": 6,
        "Kcal/Serving": 534,
        "Contributor": "Irsael Golden",
        "Diet": "Vegetarian"
    },
    "White Bean Primavera": {
        "ingredients": [
            {"ingredient": "unsalted butter", "unit": "tbsp", "quantity": 3, "category": "Dairy"},
            {"ingredient": "zucchini", "unit": "null", "quantity": 1, "category": "Produce"},
            {"ingredient": "asparagus", "unit": "oz", "quantity": 8, "category": "Produce"},
            {"ingredient": "carrot", "unit": "null", "quantity": 1, "category": "Produce"},
            {"ingredient": "garlic", "unit": "cloves", "quantity": 5, "category": "Produce"},
            {"ingredient": "frozen peas", "unit": "cup", "quantity": 1, "category": "Frozen Food"},
            {"ingredient": "scallions", "unit": "null", "quantity": 2, "category": "Produce"},
            {"ingredient": "red-pepper flakes", "unit": "tsp", "quantity": 0.5, "category": "Condiments & Spices"},
            {"ingredient": "dried oregano", "unit": "tsp", "quantity": 0.5, "category": "Condiments & Spices"},
            {"ingredient": "cannellini beans", "unit": "oz", "quantity": 45, "category": "Canned Goods"},
            {"ingredient": "heavy cream", "unit": "cup", "quantity": 0.75, "category": "Dairy"},
            {"ingredient": "lemon", "unit": "null", "quantity": 1, "category": "Produce"},
            {"ingredient": "parmesan", "unit": "oz", "quantity": 2, "category": "Dairy"},
            {"ingredient": "Dijon mustard", "unit": "tbsp", "quantity": 1, "category": "Condiments & Spices"},
            {"ingredient": "basil", "unit": "leaves", "quantity": 5, "category": "Produce"}
        ],
        "url": "https://cooking.nytimes.com/recipes/1023182-white-bean-primavera",
        "Type": "Main",
        "Servings": 4,
        "Kcal/Serving": 540,
        "Contributor": "Irsael Golden",
        "Diet": "Omnivorous"
    }
}

# Initialize the shopping list as a defaultdict to sum quantities of shared ingredients
shopping_list = defaultdict(float)

# Create a multi-select dropdown to select recipes
selected_recipes = st.multiselect("Select Recipes:", list(recipes.keys()))

# Quantity format function
def format_quantity(quantity, unit):
    if unit == "null":
        return str(int(quantity))
    elif quantity.is_integer():
        return str(int(quantity)) + " " + unit
    else:
        return "{:.2f}".format(quantity) + " " + unit

#  Shopping list generator function!
def generate_shopping_list(selected_recipes, recipes):
    shopping_list = defaultdict(float)
    selected_recipe_info = []  # List to store selected recipes and URLs

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

        # Add selected recipe and its URL to the list
        selected_recipe_info.append((recipe_name, recipe["url"]))

    return shopping_list, selected_recipe_info

# Display shopping list organized by category with items sorted alphabetically
if st.button("Generate Shopping List"):
    shopping_list, selected_recipe_info = generate_shopping_list(selected_recipes, recipes)

    # Sort the categories alphabetically
    categories = sorted(set(category for (category, _, _) in shopping_list.keys()))
    
    for category in categories:
        st.subheader(f"{category}:")
        
        # Sort the items within each category alphabetically
        sorted_items = sorted([(ingredient, unit, quantity) for (cat, ingredient, unit), quantity in shopping_list.items() if cat == category], key=lambda x: x[0])
        
        for ingredient, unit, total_quantity in sorted_items:
            formatted_quantity = format_quantity(total_quantity, unit)
            st.write(f"- {formatted_quantity} {ingredient}")

    # Display selected recipes and their URLs
    st.subheader("Selected Recipes and URLs:")
    for recipe_name, url in selected_recipe_info:
        st.write(f"- {recipe_name}: {url}")

# Download shopping list as a .txt file with today's date
if shopping_list:
    # Get today's date and format it as MM_DD_YYYY
    today_date = datetime.today().strftime("%m_%d_%Y")
    # Create the custom filename
    filename = f"ShoppingList_{today_date}.txt"

    txt_data = "\n\n".join([f"{category}:\n" + "\n".join([f"- {format_quantity(quantity, unit)} {ingredient}" for (cat, ingredient, unit), quantity in shopping_list.items() if cat == category]) for category in categories])
    
    # Include selected recipes and URLs in the .txt file content
    txt_data += "\n\nSelected Recipes and URLs:\n"
    for recipe_name, url in selected_recipe_info:
        txt_data += f"- {recipe_name}: {url}\n"

    # Create a temporary file and write the data to it
    with open(filename, "w") as f:
        f.write(txt_data)

    # Use click to create a download link with the custom filename
    st.subheader("Download Shopping List")
    with open(filename, "rb") as f:
        st.download_button(label=f"Download Shopping List", data=f, key="download_btn", file_name=filename)


# Create a DataFrame with all recipes from the dictionary
all_recipes_info = {
    "Recipe Name": list(recipes.keys()),
    "# of Servings": [recipes[recipe]["Servings"] for recipe in recipes],
    "Kcal/Serving": [recipes[recipe]["Kcal/Serving"] for recipe in recipes],
    "Diet": [recipes[recipe]["Diet"] for recipe in recipes],
    "Main/Side": [recipes[recipe]["Type"] for recipe in recipes],
    "Contributor": [recipes[recipe]["Contributor"] for recipe in recipes],
    "Link": [recipes[recipe]["url"] for recipe in recipes],
}

all_recipes_df = pd.DataFrame(all_recipes_info)


# Display the DataFrame
st.subheader("Recipe Data Frame:")
st.write("Apply filters to tailor your recipe search.")
# st.dataframe(all_recipes_df)

# Determine which ingredients are in season
# Define a dictionary of ingredient seasons with start and end dates
# seasonal_ingredients = {
#     "Italian parsley": {"start_date": datetime(2023, 3,1), "end_date": datetime(2023, 6,30)},
#     "Persian cucumbers": {"start_date": datetime(2023, 5, 15), "end_date": datetime(2023, 9, 15)},
#     "asparagus": {"start_date": datetime(2023, 3, 1), "end_date": datetime(2023, 6, 30)},
#     "avocado": {"start_date": datetime(2023, 2, 1), "end_date": datetime(2023, 10, 31)},
#     "baby arugula": {"start_date": datetime(2023, 3, 1), "end_date": datetime(2023, 11, 30)},
#     "basil": {"start_date": datetime(2023, 5, 1), "end_date": datetime(2023, 10, 31)},
#     "breakfast radish": {"start_date": datetime(2023, 8, 1), "end_date": datetime(2023, 9, 30)},
#     "broccoli": {"start_date": datetime(2023, 3, 1), "end_date": datetime(2023, 12, 31)},
    # "brussel sprouts": {"start_date": datetime(2023, , ), "end_date": datetime(2023, , )},
    # "butter lettuce": {"start_date": datetime(2023, , ), "end_date": datetime(2023, , )},
    # "carrot": {"start_date": datetime(2023, , ), "end_date": datetime(2023, , )},
    # "celery stalk": {"start_date": datetime(2023, , ), "end_date": datetime(2023, , )},
    # "celery": {"start_date": datetime(2023, , ), "end_date": datetime(2023, , )},
    # "cherry tomatoes": {"start_date": datetime(2023, , ), "end_date": datetime(2023, , )},
    # "chives": {"start_date": datetime(2023, , ), "end_date": datetime(2023, , )},
    # "cilantro": {"start_date": datetime(2023, , ), "end_date": datetime(2023, , )},
    # "fennel bulb": {"start_date": datetime(2023, , ), "end_date": datetime(2023, , )},
    # "fresh dill": {"start_date": datetime(2023, , ), "end_date": datetime(2023, , )},
    # "fresh tarragon": {"start_date": datetime(2023, , ), "end_date": datetime(2023, , )},
    # "fresh thyme": {"start_date": datetime(2023, , ), "end_date": datetime(2023, , )},
    # "garlic": {"start_date": datetime(2023, , ), "end_date": datetime(2023, , )},
    # "ginger": {"start_date": datetime(2023, , ), "end_date": datetime(2023, , )},
    # "grapefruit": {"start_date": datetime(2023, , ), "end_date": datetime(2023, , )},
    # "green coleslaw mix": {"start_date": datetime(2023, , ), "end_date": datetime(2023, , )},
    # "jalapeño": {"start_date": datetime(2023, , ), "end_date": datetime(2023, , )},
    # "large onion": {"start_date": datetime(2023, , ), "end_date": datetime(2023, , )},
    # "large red onion": {"start_date": datetime(2023, , ), "end_date": datetime(2023, , )},
    # "large yellow onion": {"start_date": datetime(2023, , ), "end_date": datetime(2023, , )},
    # "lemon": {"start_date": datetime(2023, , ), "end_date": datetime(2023, , )},
    # "lime": {"start_date": datetime(2023, , ), "end_date": datetime(2023, , )},
    # "medium yellow onion": {"start_date": datetime(2023, , ), "end_date": datetime(2023, , )},
    # "mint": {"start_date": datetime(2023, , ), "end_date": datetime(2023, , )},
    # "mint, basil, parsley or dill": {"start_date": datetime(2023, , ), "end_date": datetime(2023, , )},
    # "mixed mushrooms": {"start_date": datetime(2023, , ), "end_date": datetime(2023, , )},
    # "orange": {"start_date": datetime(2023, , ), "end_date": datetime(2023, , )},
    # "pineapple": {"start_date": datetime(2023, , ), "end_date": datetime(2023, , )},
    # "plum tomatoes": {"start_date": datetime(2023, , ), "end_date": datetime(2023, , )},
    # "poblano or green bell pepper": {"start_date": datetime(2023, , ), "end_date": datetime(2023, , )},
    # "portobello mushrooms": {"start_date": datetime(2023, , ), "end_date": datetime(2023, , )},
    # "radishes": {"start_date": datetime(2023, , ), "end_date": datetime(2023, , )},
    # "red bell pepper": {"start_date": datetime(,2023 , ), "end_date": datetime(2023, , )},
    # "red grapes": {"start_date": datetime(2023, , ), "end_date": datetime(2023, , )},
    # "red onion": {"start_date": datetime(2023, , ), "end_date": datetime(2023, , )},
    # "red, orange, or yellow bell peppers": {"start_date": datetime(2023, , ), "end_date": datetime(2023, , )},
    # "russet potatoes": {"start_date": datetime(2023, , ), "end_date": datetime(2023, , )},
    # "scallions": {"start_date": datetime(2023, , ), "end_date": datetime(2023, , )},
    # "shallots": {"start_date": datetime(2023, , ), "end_date": datetime(2023, , )},
    # "small yellow onion": {"start_date": datetime(2023, , ), "end_date": datetime(2023, , )},
    # "spinach": {"start_date": datetime(2023, , ), "end_date": datetime(2023, , )},
    # "stone fruit": {"start_date": datetime(2023, , ), "end_date": datetime(2023, , )},
    # "sweet or mild peppers": {"start_date": datetime(2023, , ), "end_date": datetime(2023, , )},
    # "white onion": {"start_date": datetime(2023, , ), "end_date": datetime(2023, , )},
    # "yellow onion": {"start_date": datetime(2023, , ), "end_date": datetime(2023, , )},
    # "zucchini": {"start_date": datetime(2023, , ), "end_date": datetime(2023, , )},
# }

# Add a new column "In Season" to your DataFrame based on today's date
# Add a new column "In Season" to your DataFrame based on today's date
# today_date = datetime.now()

# def is_ingredient_in_season(ingredient_season):
#     today_month_day = today_date.strftime("%m-%d")
#     start_month_day = ingredient_season["start_date"].strftime("%m-%d")
#     end_month_day = ingredient_season["end_date"].strftime("%m-%d")
    
#     # Check if today's month and day fall within the specified range
#     return start_month_day <= today_month_day <= end_month_day

# all_recipes_df["In Season"] = all_recipes_df.apply(lambda row: is_ingredient_in_season(seasonal_ingredients.get(row["Recipe Name"], {})), axis=1)

# Create a layout with four columns for filters
col1, col2, col3 = st.columns(3)


# Filter Recipes by Diet
with col1:
    selected_diet = st.selectbox("Select Diet:", ["All"] + list(set(all_recipes_df["Diet"])))
    if selected_diet != "All":
        all_recipes_df = all_recipes_df[all_recipes_df["Diet"] == selected_diet]

# Filter Recipes by Maximum Kcal per Serving
with col2:
    max_kcal = st.slider("Maximum Kcal per Serving:", 0, max(all_recipes_df["Kcal/Serving"]), max(all_recipes_df["Kcal/Serving"]))
    all_recipes_df = all_recipes_df[all_recipes_df["Kcal/Serving"] <= max_kcal]

# Filter Recipes by Type
with col3:
    selected_type = st.selectbox("Select Recipe Type:", ["All"] + list(set(all_recipes_df["Main/Side"])))
    if selected_type != "All":
        all_recipes_df = all_recipes_df[all_recipes_df["Main/Side"] == selected_type]

# Display the filtered DataFrame
st.dataframe(all_recipes_df)
st.download_button(label = 'Download Recipe Spreadsheet', 
                   data = all_recipes_df.to_csv(), 
                   mime='text/csv', 
                   file_name='RecipeSpreadsheet')
