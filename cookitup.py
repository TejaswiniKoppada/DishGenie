# Title: CookItUp - Deep Learning and CNN for Smart Cooking Solutions
# FY25-Q1-S1-01/23-Ver:1.0
# Author: Tejaswini (Developer)
# Releases: FY25-Q1-S1-01/23-Ver:1.0-CHG-Designed UI using Flask integration for login/sign-up.
# Releases: FY25-Q1-S2-01/23-Ver:2.0-CHG-Enhancement - User Authentication System (login(), signup())
# Releases: FY25-Q1-S3-01/23-Ver:2.0-CHG-Enhancement - Dashboard, Pantry Tracker.
# Releases: FY25-Q1-S4-01/23-Ver:2.0-CHG-Enhancement - Created custom dataset for recipes and trained the model file (recipe_model.keras, tokenizer.pkl, label_encoder.pkl).
# Releases: FY25-Q1-S5-01/23-Ver:2.0-CHG-Enhancement - Integrated the .jpg custom dataset into the code.
# Releases: FY25-Q1-S6-01/23-Ver:2.0-CHG-Enhancement - implemented pantry tracker ui and functionality.(get_inventory())
# Releases: FY25-Q1-S7-01/23-Ver:2.0-CHG-Enhancement - Updated the code to add delete, add and minus buttons in pantry table.(delete_ingredient())
# Releases: FY25-Q1-S8-01/23-Ver:2.0-CHG-Enhancement - Functionality added for Surprise recipe generation(surprise_recipe())
# Releases: FY25-Q1-S9-01/23-Ver:2.0-CHG-Enhancement - Connected saved_recipes.csv to update the saved recipes as per the user.(save_recipe(),saved_recipe())
# Releases: FY25-Q1-S10-01/23-Ver:2.0-CHG-Enhancement - recipe_dispaly to call all the columns in the predicted recipe.
# Releases: FY25-Q1-S11-01/23-Ver:2.0-CHG-Enhancement - ingredient_selection to predict all the recipes related.(generate_recipe())
# Releases: FY25-Q1-S12-01/23-Ver:2.0-CHG-Enhancement - Modified the pantry ui to toggle button to upload image ingredients(update_ingredient_status())
# Releases: FY25-Q1-S13-01/23-Ver:2.0-CHG-Enhancement - Pre trained model traing using MobileNetV5 and integration in the code..(predict_ingredient())(ingredient_classifier.h5 , class_indicies.json)
# Releases: FY25-Q1-S14-01/23-Ver:2.0-CHG-Enhancement - Working on helper functions.

# Importing necessary libraries for the Flask application, data manipulation, and deep learning.
from flask import Flask, render_template, request, jsonify, redirect, url_for, session, send_from_directory
import pandas as pd  # For data manipulation and analysis using DataFrames.
import os  # For interacting with the operating system, such as file paths and directories.
import tensorflow as tf  # For deep learning and neural network operations.
import pickle  # For serializing and deserializing Python objects (e.g., saving/loading models).
import numpy as np  # For numerical computations and array manipulations.
import keras  # High-level neural networks API, running on top of TensorFlow.
from keras import layers  # For defining neural network layers.
import chardet  # For detecting the encoding of files.
from keras.preprocessing import image  # For image preprocessing and augmentation.
import json  # For working with JSON data (e.g., loading/saving configurations).

# Initializing the Flask application and setting the secret key for session management  
app = Flask(__name__, static_folder="static")  
app.secret_key = "your_secret_key"  

# Defining the upload folder path and creating it if it doesn't exist  
UPLOAD_FOLDER = os.path.join(app.static_folder, 'images')  
if not os.path.exists(UPLOAD_FOLDER):  
    os.makedirs(UPLOAD_FOLDER)  

# Defining file paths for user data, ingredients, datasets, model, tokenizer, and label encoder  
USERS_FILE = "cookitupusers.xlsx"
ALL_INGREDIENTS_FILE = r"C:\Users\prudh\Desktop\Final cook\Final cook\all_ingredients.csv"
REFINARY_FILE = r"C:\Users\prudh\Desktop\Final cook\Final cook\refinary.csv"
DATASET_FILE = r"C:\Users\prudh\Desktop\Final cook\Final cook\my_dataset.csv"
MODEL_FILE = r"C:\Users\prudh\Desktop\Final cook\Final cook\recipe_model.keras"
TOKENIZER_FILE = r"C:\Users\prudh\Desktop\Final cook\Final cook\tokenizer.pkl"
LABEL_ENCODER_FILE = r"C:\Users\prudh\Desktop\Final cook\Final cook\label_encoder.pkl"
WHOLE_DATASET_FILE = r"C:\Users\prudh\Desktop\Final cook\Final cook\whole dataset.csv"



# Checking if required files exist; if not, creating empty files with predefined columns  
if not os.path.exists(USERS_FILE):
    pd.DataFrame(columns=["username", "email", "password"]).to_excel(USERS_FILE, index=False)
if not os.path.exists(ALL_INGREDIENTS_FILE):
    pd.DataFrame(columns=["ingredient"]).to_csv(ALL_INGREDIENTS_FILE, index=False, header=False)
if not os.path.exists(REFINARY_FILE):
    pd.DataFrame(columns=["email", "ingredient", "status"]).to_csv(REFINARY_FILE, index=False)


# Loading the trained Keras model with custom objects  
custom_objects = {"InputLayer": lambda config: layers.InputLayer.from_config(config)}  
with tf.keras.utils.custom_object_scope(custom_objects):  
    model = tf.keras.models.load_model(MODEL_FILE, compile=False)  

# Loading the tokenizer and label encoder from saved pickle files  
with open(TOKENIZER_FILE, "rb") as f:  
    tokenizer = pickle.load(f)  

with open(LABEL_ENCODER_FILE, "rb") as f:  
    label_encoder = pickle.load(f)  



# Detecting the file encoding and loading the whole dataset while handling bad lines  
with open(WHOLE_DATASET_FILE, "rb") as f:  
    result = chardet.detect(f.read())  
    detected_encoding = result["encoding"]  

whole_dataset = pd.read_csv(WHOLE_DATASET_FILE, encoding=detected_encoding, on_bad_lines="skip")  



# Detecting the file encoding and loading the dataset while handling bad lines  
with open(DATASET_FILE, "rb") as f:  
    result = chardet.detect(f.read())  
    detected_encoding = result["encoding"]  

dataset = pd.read_csv(DATASET_FILE, encoding=detected_encoding, on_bad_lines="skip")  



# Load the model and class indices
model = tf.keras.models.load_model('ingredient_classifier (2).h5')
with open('class_indices (1).json', 'r') as f:
    class_indices = json.load(f)
class_names = {v: k for k, v in class_indices.items()}


# Function to validate user credentials by checking the stored user data  
def validate_user(email, password):  
    users = pd.read_excel(USERS_FILE)  
    user = users[(users["email"] == email) & (users["password"] == password)]  
    return not user.empty  

# Function to register a new user by adding their details to the user file  
def register_user(username, email, password):  
    try:  
        users = pd.read_excel(USERS_FILE)  
        if email in users["email"].values:  
            return False, "User already exists."  

        new_user = pd.DataFrame({"username": [username], "email": [email], "password": [password]})  
        users = pd.concat([users, new_user], ignore_index=True)  
        users.to_excel(USERS_FILE, index=False)  

        return True, "Registration successful."  
    except Exception as e:  
        return False, f"Error during registration: {e}"  

# Function to load user data from the Excel file safely  
def load_users():  
    """Load user data from the Excel file safely."""  
    try:  
        df = pd.read_excel(USERS_FILE, engine='openpyxl')  

        # Ensure required columns exist, else create an empty DataFrame  
        if "Email" not in df or "Password" not in df:  
            df = pd.DataFrame(columns=["Username", "Email", "Password"])  

        # Standardizing email and password formatting  
        df["Email"] = df["Email"].astype(str).str.strip().str.lower()  
        df["Password"] = df["Password"].astype(str).str.strip()  

        return df  
    except Exception:  
        return pd.DataFrame(columns=["Username", "Email", "Password"])  
    

# Function to add an ingredient to the user's inventory or update its status  
def add_ingredient(email, ingredient):  
    try:  
        all_ingredients = pd.read_csv(ALL_INGREDIENTS_FILE, header=None, names=["ingredient"])  
        refinary = pd.read_csv(REFINARY_FILE)  

        # Check if the ingredient exists in the dataset  
        if ingredient.lower() not in all_ingredients["ingredient"].str.lower().values:  
            return False, "No Recipe found with the input ingredient."  

        # Check if the ingredient already exists in the user's inventory  
        existing = refinary[(refinary["email"] == email) & (refinary["ingredient"].str.lower() == ingredient.lower())]  

        if not existing.empty:  
            # If the ingredient exists but is marked as "Unavailable", update its status to "Available"  
            if existing.iloc[0]["status"] == "Unavailable":  
                refinary.loc[existing.index, "status"] = "Available"  
                refinary.to_csv(REFINARY_FILE, index=False, mode="w")  # Force write  
                return True, "Ingredient status updated to Available."  
            else:  
                return False, "Ingredient already exists in the inventory."  
        else:  
            # If the ingredient does not exist, add it to the inventory  
            new_row = pd.DataFrame({"email": [email], "ingredient": [ingredient], "status": "Available"})  
            refinary = pd.concat([refinary, new_row], ignore_index=True)  
            refinary.to_csv(REFINARY_FILE, index=False, mode="w")  # Force write  
            return True, "Ingredient added successfully."  

    except Exception as e:  
        return False, f"Error adding ingredient: {e}"  

    
    
# Function to retrieve the user's ingredient inventory  
def get_user_inventory(email):  
    refinary = pd.read_csv(REFINARY_FILE)  
    return refinary[refinary["email"] == email].to_dict("records")  



# Function to normalize ingredients by converting to lowercase, stripping whitespace, and sorting  

def normalize_ingredients(ingredients):  
    """  
    Normalize ingredients by converting to lowercase, stripping whitespace, and sorting.  
    """  
    return sorted([ingredient.strip().lower() for ingredient in ingredients])  

# Function to clean and normalize recipe ingredients from the dataset  
def clean_recipe_ingredients(recipe_ingredients):  
    """  
    Clean and normalize recipe ingredients from the dataset.  
    """  
    if isinstance(recipe_ingredients, str):  
        return normalize_ingredients(recipe_ingredients.split(','))  
    return []  


# Function to predict recipes based on user-provided ingredients  

def predict_recipes(ingredients):  
    try:  
        print("Ingredients for Prediction:", ingredients)  

        # Normalize input ingredients  
        input_ingredients = normalize_ingredients(ingredients)  
        input_ingredients_str = ", ".join(input_ingredients)  
        print("Normalized Input Ingredients:", input_ingredients_str)  

        matching_recipes = []  

        # Iterate through dataset to find exact ingredient matches  
        for index, row in dataset.iterrows():  
            recipe_ingredients = clean_recipe_ingredients(row['List of ingredients'])  
            if input_ingredients == recipe_ingredients:  
                matching_recipes.append({  
                    "name": row["Recipe Name"],  
                    "time": row["Time Required (minutes)"],  
                    "cuisine": row["Style"],  
                    "confidence": 1.0  # Exact match confidence  
                })  

        if not matching_recipes:  
            print("No exact match found for the given ingredients.")  
            return [], []  

        print("Matching Recipes:", matching_recipes)  
        return matching_recipes, [1.0] * len(matching_recipes)  

    except Exception as e:  
        print("Error in predict_recipes:", str(e))  
        return [], []  


# Function to fetch the making process of a recipe from the dataset  

def get_making_process(recipe_name):  
    """  
    Fetch the making process from the whole dataset based on the recipe name.  
    """  
    try:  
        making_process = whole_dataset[whole_dataset['Recipe Name'] == recipe_name]['Making Process'].values[0]  
        return making_process  
    except IndexError:  
        return "Making process not found for the given recipe name."  

    
# Route to render the first page of the application  
@app.route("/")  
def first():  
    return render_template("first.html")  

# Route to render the login page  
@app.route("/login_page")  
def login_page():  
    return render_template("index.html")  

# Route to render the help page  
@app.route('/help')  
def help_page():  
    return render_template('help.html')  



# Route to handle user signup  

@app.route("/signup", methods=["POST"])  
def signup():  
    try:  
        data = request.get_json()  
        name = data["name"].strip()  
        email = data["email"].strip().lower()  
        password = data["password"].strip()  

        df = load_users()  

        # Check if the email is already registered  
        if email in df["Email"].values:  
            return jsonify({"status": "error", "message": "User already registered with this email."})  

        # Add the new user to the dataset  
        new_user = pd.DataFrame({"name": [name], "Email": [email], "Password": [password]})  
        df = pd.concat([df, new_user], ignore_index=True)  

        # Save the updated user list to the Excel file  
        with pd.ExcelWriter(USERS_FILE, engine='openpyxl', mode='w') as writer:  
            df.to_excel(writer, index=False)  

        return jsonify({"status": "success", "message": "User registered successfully!"})  

    except Exception as e:  
        return jsonify({"status": "error", "message": f"Server error: {str(e)}"})  

    


# Route to handle user login  

@app.route("/login", methods=["POST"])  
def login():  
    try:  
        data = request.get_json()  
        email = data.get("email", "").strip().lower()  # Normalize email  
        password = data.get("password", "").strip()  

        # Check for empty fields  
        if not email or not password:  
            return jsonify({"status": "error", "message": "All fields are required."})  

        df = load_users()  
        user = df[df["Email"].str.lower() == email]  

        # Check if the email is registered  
        if user.empty:  
            return jsonify({"status": "error", "message": "Email not registered!"})  

        # Validate password  
        if user.iloc[0]["Password"] != password:  
            return jsonify({"status": "error", "message": "Incorrect password!"})  

        session['user_email'] = email  # Store user session  

        return jsonify({"status": "success", "message": "Login successful!", "redirect": "/home"})  

    except Exception as e:  
        print(f"Login Error: {e}")  
        return jsonify({"status": "error", "message": "Server error. Please try again."})  

    
# Route to render the home page  

@app.route("/home")  
def home():  
    if 'user_email' not in session:  
        return redirect(url_for('login'))  # Redirect if the user is not logged in  

    users = pd.read_excel(USERS_FILE, dtype=str)  
    users.columns = users.columns.str.strip().str.lower()  

    # Check if the email column exists in the dataset  
    if "email" not in users.columns:  
        return "Error: 'email' column not found in the dataset", 500  

    user = users[users["email"] == session['user_email']]  

    # Check if the user exists  
    if user.empty:  
        return "Error: User not found", 404  

    user_name = user.iloc[0]["name"]  # Retrieve the user's name  

    return render_template("home.html", user_name=user_name)  



# Route to render the inventory page  

@app.route("/inventory")  
def inventory():  
    return render_template("inventory.html")  



# Route to add an ingredient to the user's inventory  

@app.route("/add_ingredient", methods=["POST"])  
def add_ingredient_route():  
    try:  
        if 'user_email' not in session:  
            return jsonify({"status": "error", "message": "User not logged in."})  

        email = session['user_email']  
        ingredient = request.json.get("ingredient").strip()  

        if not ingredient:  
            return jsonify({"status": "error", "message": "Ingredient cannot be empty."})  

        # Check if the ingredient exists in the dataset  
        all_ingredients = pd.read_csv(ALL_INGREDIENTS_FILE, header=None, names=["ingredient"])  
        if ingredient.lower() not in all_ingredients["ingredient"].str.lower().values:  
            return jsonify({"status": "error", "message": "No recipe found with the input ingredient."})  

        refinary = pd.read_csv(REFINARY_FILE)  

        # Check if the ingredient already exists in the user's inventory  
        existing = refinary[(refinary["email"] == email) & (refinary["ingredient"].str.lower() == ingredient.lower())]  

        if not existing.empty:  
            if existing.iloc[0]["status"] == "Unavailable":  
                refinary.loc[existing.index, "status"] = "Available"  
                refinary.to_csv(REFINARY_FILE, index=False)  
                return jsonify({"status": "success", "message": "Ingredient added to the pantry."})  
            else:  
                return jsonify({"status": "error", "message": "Ingredient already exists in the inventory."})  

        # Add new ingredient to the inventory  
        new_row = pd.DataFrame({"email": [email], "ingredient": [ingredient], "status": "Available"})  
        refinary = pd.concat([refinary, new_row], ignore_index=True)  
        refinary.to_csv(REFINARY_FILE, index=False)  
        return jsonify({"status": "success", "message": "Ingredient added to the pantry."})  

    except Exception as e:  
        return jsonify({"status": "error", "message": f"Server error: {str(e)}"})  


# This endpoint retrieves the logged-in user's inventory details.

@app.route("/get_inventory", methods=["GET"])
def get_inventory():
    try:
        # Retrieve the logged-in user's email from the session
        email = session.get("user_email")
        if not email:
            return jsonify({"status": "error", "message": "User not logged in."})

        # Check if the inventory file exists; if not, return an empty inventory
        if not os.path.exists(REFINARY_FILE):
            return jsonify({"status": "success", "inventory": []})

        # Load the inventory data from the CSV file
        refinary = pd.read_csv(REFINARY_FILE)

        # Validate if the required columns exist in the file
        if "email" not in refinary.columns or "ingredient" not in refinary.columns:
            return jsonify({"status": "error", "message": "Invalid inventory data format."})

        # Filter the inventory based on the logged-in user's email
        user_inventory = refinary[refinary["email"] == email].to_dict("records")

        # Return the user's inventory data in JSON format
        return jsonify({"status": "success", "inventory": user_inventory})

    except Exception as e:
        # Handle any server errors and return an error response
        return jsonify({"status": "error", "message": f"Server error: {str(e)}"})



# This endpoint handles recipe selection based on user-provided ingredients.

@app.route("/recipe_selection", methods=["GET", "POST"])
def recipe_selection():
    if request.method == "GET":
        # Render the recipe selection page
        return render_template("recipe_selection.html")
    
    elif request.method == "POST":
        try:
            # Retrieve JSON data from the request
            data = request.json
            ingredients = data.get("ingredients", [])

            print("Received Ingredients:", ingredients)  # Debugging log

            # Check if ingredients are provided
            if not ingredients:
                return jsonify({"success": False, "message": "No ingredients provided."})

            # Predict recipes based on the given ingredients
            predicted_recipes, probabilities = predict_recipes(ingredients)
            print("Predicted Recipes:", predicted_recipes)  # Debugging log

            # Check if any recipes were predicted
            if not predicted_recipes:
                return jsonify({"success": False, "message": "No recipes found. Check model output."})

            # Store predicted recipes and probabilities in session
            session['predicted_recipes'] = predicted_recipes
            session['probabilities'] = [float(prob) for prob in probabilities]

            # Redirect to the recipe display page
            return jsonify({"success": True, "redirect": url_for('recipe_display')})

        except Exception as e:
            print("Error in /recipe_selection:", str(e))  # Debugging log
            return jsonify({"success": False, "message": f"Server Error: {str(e)}"})



    

# This endpoint generates recipes based on user-provided ingredients.

@app.route("/generate_recipe", methods=["POST"])
def generate_recipe():
    try:
        # Retrieve JSON data from the request
        data = request.json
        ingredients = data.get("ingredients", [])

        print("Received Ingredients:", ingredients)  # Debugging log

        # Check if ingredients are provided
        if not ingredients:
            return jsonify({"success": False, "message": "No ingredients provided."})

        # Predict recipes based on the given ingredients
        predicted_recipes, probabilities = predict_recipes(ingredients)
        print("Predicted Recipes:", predicted_recipes)  # Debugging log

        # Check if any recipes were predicted
        if not predicted_recipes:
            return jsonify({"success": False, "message": "No recipes found. Check model output."})

        # Mark ingredients as "Unavailable" in the inventory
        email = session.get("user_email")
        if email:
            refinary = pd.read_csv(REFINARY_FILE)
            for ingredient in ingredients:
                # Update the ingredient status to "Unavailable" for the logged-in user
                refinary.loc[
                    (refinary["email"] == email) & (refinary["ingredient"].str.lower() == ingredient.lower()),
                    "status"
                ] = "Unavailable"
            # Save the updated inventory back to the CSV file
            refinary.to_csv(REFINARY_FILE, index=False)

        # Store predicted recipes and probabilities in session
        session['predicted_recipes'] = predicted_recipes
        session['probabilities'] = [float(prob) for prob in probabilities]

        # Redirect to the recipe display page
        return jsonify({
            "success": True,
            "redirect": url_for('recipe_display')  # Ensure this URL is correct
        })

    except Exception as e:
        print("Error in /generate_recipe:", str(e))  # Debugging log
        return jsonify({"success": False, "message": f"Server Error: {str(e)}"})

    

# This endpoint displays the predicted recipes for the logged-in user.

@app.route("/recipe_display")
def recipe_display():
    try:
        if 'user_email' not in session:
            return redirect(url_for('login'))

        predicted_recipes = session.get('predicted_recipes', [])
        probabilities = session.get('probabilities', [])

        if not predicted_recipes:
            return render_template("recipe_display.html", message="No recipes found.")

        return render_template("recipe_display.html", recipes=predicted_recipes)

    except Exception as e:
        return jsonify({"status": "error", "message": f"Server error: {str(e)}"})

    
# This endpoint retrieves and displays the details of a selected recipe.

@app.route("/recipe_details/<recipe_name>")
def recipe_details(recipe_name):
    try:
        if 'user_email' not in session:
            return redirect(url_for('login'))

        # Fetch the recipe details from the dataset
        recipe = dataset[dataset['Recipe Name'] == recipe_name].iloc[0]
        
        # Fetch the making process from the dataset
        making_process = get_making_process(recipe_name)

        recipe_details = {
            "name": recipe["Recipe Name"],
            "time": recipe["Time Required (minutes)"],
            "style": recipe["Style"],
            "recipe": making_process,
            "protein": recipe["Protein (g)"],
            "carbs": recipe["Carbohydrates (g)"],
            "fats": recipe["Fats (g)"],
            "sides": recipe["Sides"],
            "youtube_link": f"https://www.youtube.com/results?search_query={recipe['Recipe Name'].replace(' ', '+')}"
        }

        return render_template("recipe_details.html", recipe=recipe_details)

    except Exception as e:
        return jsonify({"status": "error", "message": f"Server error: {str(e)}"})

    
# This endpoint allows users to save their favorite recipes.

@app.route("/save_recipe", methods=["POST"])
def save_recipe():
    try:
        if 'user_email' not in session:
            return jsonify({"status": "error", "message": "User not logged in."})

        data = request.json
        recipe_name = data.get("recipe_name")

        # Fetch the recipe details from the dataset
        recipe = dataset[dataset['Recipe Name'] == recipe_name].iloc[0]

        # Add the user's email to the recipe details
        recipe["user_email"] = session['user_email']

        # Save the recipe to a new file or database (for simplicity, using a CSV file)
        saved_recipes_file = "saved_recipes.csv"

        # Define the columns for the saved recipes file
        columns = [*dataset.columns, "user_email"]

        # Check if the file exists and is not empty
        if not os.path.exists(saved_recipes_file) or os.path.getsize(saved_recipes_file) == 0:
            # Create the file with the correct columns if it doesn't exist or is empty
            pd.DataFrame(columns=columns).to_csv(saved_recipes_file, index=False)

        # Load the saved recipes
        saved_recipes = pd.read_csv(saved_recipes_file)

        # Check if the recipe is already saved by the user
        if not ((saved_recipes["Recipe Name"] == recipe_name) & (saved_recipes["user_email"] == session['user_email'])).any():
            # Convert the recipe Series to a DataFrame and append it
            recipe_df = pd.DataFrame([recipe])
            saved_recipes = pd.concat([saved_recipes, recipe_df], ignore_index=True)
            saved_recipes.to_csv(saved_recipes_file, index=False)
            return jsonify({"status": "success", "message": "Recipe saved successfully!"})
        else:
            return jsonify({"status": "error", "message": "Recipe already saved."})

    except Exception as e:
        print(f"Error in save_recipe: {str(e)}")  # Debugging
        return jsonify({"status": "error", "message": f"Server error: {str(e)}"})

    

# This endpoint displays the list of recipes saved by the logged-in user.

@app.route("/saved_recipes")
def saved_recipes():
    try:
        if 'user_email' not in session:
            return redirect(url_for('login'))

        # Load saved recipes from the CSV file
        saved_recipes_file = "saved_recipes.csv"
        if not os.path.exists(saved_recipes_file):
            return render_template("saved_recipes.html", recipes=[])

        saved_recipes = pd.read_csv(saved_recipes_file)
        # Filter recipes saved by the logged-in user
        user_saved_recipes = saved_recipes[saved_recipes["user_email"] == session['user_email']]
        return render_template("saved_recipes.html", recipes=user_saved_recipes.to_dict("records"))

    except Exception as e:
        return jsonify({"status": "error", "message": f"Server error: {str(e)}"})


# This endpoint allows users to delete a saved recipe from their list.

@app.route("/delete_recipe", methods=["POST"])
def delete_recipe():
    try:
        if 'user_email' not in session:
            return jsonify({"status": "error", "message": "User not logged in."})

        data = request.json
        recipe_name = data.get("recipe_name")

        # Load saved recipes from the CSV file
        saved_recipes_file = "saved_recipes.csv"
        if not os.path.exists(saved_recipes_file):
            return jsonify({"status": "error", "message": "No saved recipes found."})

        saved_recipes = pd.read_csv(saved_recipes_file)
        # Delete only the recipe saved by the logged-in user
        saved_recipes = saved_recipes[~((saved_recipes["Recipe Name"] == recipe_name) & (saved_recipes["user_email"] == session['user_email']))]
        saved_recipes.to_csv(saved_recipes_file, index=False)

        return jsonify({"status": "success", "message": "Recipe deleted successfully!"})

    except Exception as e:
        return jsonify({"status": "error", "message": f"Server error: {str(e)}"})

# This endpoint allows users to delete an ingredient from their inventory.

@app.route("/delete_ingredient", methods=["POST"])
def delete_ingredient():
    try:
        if 'user_email' not in session:
            return jsonify({"status": "error", "message": "User not logged in."})

        data = request.json
        ingredient = data.get("ingredient").strip()

        if not ingredient:
            return jsonify({"status": "error", "message": "Ingredient cannot be empty."})

        # Load the refinary data
        refinary = pd.read_csv(REFINARY_FILE)

        # Remove the ingredient for the logged-in user
        refinary = refinary[~((refinary["email"] == session['user_email']) & (refinary["ingredient"].str.lower() == ingredient.lower()))]

        # Save the updated refinary data
        refinary.to_csv(REFINARY_FILE, index=False)

        return jsonify({"status": "success", "message": "Ingredient deleted successfully!"})

    except Exception as e:
        return jsonify({"status": "error", "message": f"Server error: {str(e)}"})
# This endpoint randomly selects a recipe from the dataset and displays its details.

@app.route("/surprise_recipe")
def surprise_recipe():
    try:
        if 'user_email' not in session:
            return redirect(url_for('login'))

        # Select a random recipe from the dataset
        random_recipe = dataset.sample(n=1).iloc[0]
        recipe_name = random_recipe["Recipe Name"]
        making_process = get_making_process(recipe_name)  # Fetch making process from the whole dataset

        recipe_details = {
            "name": recipe_name,
            "time": random_recipe["Time Required (minutes)"],
            "cuisine": random_recipe["Style"],
            "recipe": making_process,  # Use the making process from the whole dataset
            "protein": random_recipe["Protein (g)"],
            "carbs": random_recipe["Carbohydrates (g)"],
            "fats": random_recipe["Fats (g)"],
            "sides": random_recipe["Sides"],
            "ingredients": clean_recipe_ingredients(random_recipe['List of ingredients'])
        }

        return render_template("surprise_recipe.html", recipe=recipe_details)

    except Exception as e:
        return jsonify({"status": "error", "message": f"Server error: {str(e)}"})


# Function to preprocess the image
def preprocess_image(img_path, target_size=(128, 128)):
    img = image.load_img(img_path, target_size=target_size)
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
    img_array /= 255.0  # Normalize the image
    return img_array

# Endpoint to predict the ingredient from an uploaded image and update the user's inventory
@app.route("/predict_ingredient", methods=["POST"])
def predict_ingredient():
    if 'file' not in request.files:
        return jsonify({"status": "error", "message": "No file uploaded."})

    file = request.files['file']
    if file.filename == '':
        return jsonify({"status": "error", "message": "No file selected."})

    # Save the file temporarily
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    try:
        # Preprocess the image
        img_array = preprocess_image(file_path)

        # Make prediction
        predictions = model.predict(img_array)
        predicted_class_index = np.argmax(predictions, axis=1)[0]
        predicted_class_name = class_names[predicted_class_index]

        # Check if the ingredient exists in all_ingredients.csv
        all_ingredients = pd.read_csv(ALL_INGREDIENTS_FILE, header=None, names=["ingredient"])
        if predicted_class_name.lower() not in all_ingredients["ingredient"].str.lower().values:
            return jsonify({"status": "error", "message": "Ingredient not found in dataset."})

        # Add the ingredient to refinary.csv
        email = session.get('user_email')
        if not email:
            return jsonify({"status": "error", "message": "User not logged in."})

        refinary = pd.read_csv(REFINARY_FILE)
        existing = refinary[(refinary["email"] == email) & (refinary["ingredient"].str.lower() == predicted_class_name.lower())]
        
        if not existing.empty:
            if existing.iloc[0]["status"] == "Unavailable":
                refinary.loc[existing.index, "status"] = "Available"
                refinary.to_csv(REFINARY_FILE, index=False, mode="w")  # Force write
                inventory = get_user_inventory(email)  # Fetch updated inventory
                return jsonify({"status": "success", "message": "Ingredient status updated to Available.", "ingredient": predicted_class_name, "inventory": inventory})
            else:
                return jsonify({"status": "error", "message": "Ingredient already exists in the inventory."})
        else:
            new_row = pd.DataFrame({"email": [email], "ingredient": [predicted_class_name], "status": "Available"})
            refinary = pd.concat([refinary, new_row], ignore_index=True)
            refinary.to_csv(REFINARY_FILE, index=False, mode="w")  # Force write
            inventory = get_user_inventory(email)  # Fetch updated inventory
            return jsonify({"status": "success", "message": "Ingredient added successfully.", "ingredient": predicted_class_name, "inventory": inventory})

    except Exception as e:
        return jsonify({"status": "error", "message": f"Error predicting ingredient: {str(e)}"})

    finally:
        # Clean up the temporary file
        if os.path.exists(file_path):
            os.remove(file_path)


            
# Endpoint to log out the user and clear the session
@app.route("/logout")
def logout():
    session.pop('user_email', None)  # Clear the user session
    return redirect(url_for('first'))  # Redirect to the home page



# Endpoint to update the status of an ingredient for a logged-in user
@app.route("/update_ingredient_status", methods=["POST"])
def update_ingredient_status():
    try:
        if 'user_email' not in session:
            return jsonify({"status": "error", "message": "User not logged in."})

        data = request.json
        ingredient = data.get("ingredient").strip()
        status = data.get("status").strip()

        if not ingredient or not status:
            return jsonify({"status": "error", "message": "Ingredient or status cannot be empty."})

        # Load the refinary data
        refinary = pd.read_csv(REFINARY_FILE)

        # Update the ingredient status for the logged-in user
        refinary.loc[
            (refinary["email"] == session['user_email']) & (refinary["ingredient"].str.lower() == ingredient.lower()),
            "status"
        ] = status

        # Save the updated refinary data
        refinary.to_csv(REFINARY_FILE, index=False)

        return jsonify({"status": "success", "message": "Ingredient status updated successfully!"})

    except Exception as e:
        return jsonify({"status": "error", "message": f"Server error: {str(e)}"})



# Endpoint to check if an ingredient exists in the dataset
@app.route("/check_ingredient", methods=["POST"])
def check_ingredient():
    try:
        data = request.json
        ingredient = data.get("ingredient").strip().lower()

        if not ingredient:
            return jsonify({"exists": False, "message": "Ingredient cannot be empty."})

        # Check if the ingredient exists in all_ingredients.csv
        all_ingredients = pd.read_csv(ALL_INGREDIENTS_FILE, header=None, names=["ingredient"])
        exists = ingredient in all_ingredients["ingredient"].str.lower().values

        return jsonify({"exists": exists})

    except Exception as e:
        return jsonify({"exists": False, "message": f"Server error: {str(e)}"})

# Run the Flask application on port 6777 with debug mode enabled
if __name__ == "__main__":
    app.run(debug=True, port=6777)

