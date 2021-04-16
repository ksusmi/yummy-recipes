"""CRUD operations."""

from model import db, User, DishType, Cuisine, Diet, Ingredient, RecipeIngredient, Recipe, Rating, connect_to_db
#import model from model



# Functions start here!

def create_user(fname, lname, email, password, mobile_no):
    """Create and return a new user."""


    user = User(fname = fname, lname=lname, email=email, password=password, mobile_no = mobile_no)

    db.session.add(user)
    db.session.commit()

    return user

def create_dishtype(dishtype_name):
    """Create and return the dishtype for the recipe """

    dishtype = DishType(dishtype_name = dishtype_name)

    db.session.add(dishtype)
    db.session.commit()

    return dishtype

def create_cuisine(cuisine_name):
    """Create and return the type of cuisine for the recipe """

    cuisine = Cuisine(cuisine_name = cuisine_name)

    db.session.add(cuisine)
    db.session.commit()

    return cuisine

def create_diet(diet_name):
    """Create and return the type of diet for the recipe """

    diet = Diet(diet_name = diet_name)

    db.session.add(diet)
    db.session.commit()

    return diet

def create_ingredient(ingredient, unit):
    """Create and return the ingredients required """

    ingredient = Ingredient(ingredient=ingredient, unit=unit)

    db.session.add(ingredient)
    db.session.commit()

    return ingredient


def create_recipeingredient(ingredient_id, recipe_id, quantity):
    """Create and return the recipe ingredients for the recipe """

    recipeingredient = RecipeIngredient(ingredient_id=ingredient_id, recipe_id=recipe_id, quantity= quantity)

    db.session.add(recipeingredient)
    db.session.commit()

    return recipeingredient

def create_recipe(title, description, prep_time, cook_time, dishtype_id, cuisine_id,diet_id, instructions,url):
    """Create and return the recipe created """

    recipe = Recipe(title = title, description= description, prep_time= prep_time, cook_time=cook_time, dishtype_id= dishtype_id, cuisine_id=cuisine_id, diet_id=diet_id, instructions= instructions,url=url)

    db.session.add(recipe)
    db.session.commit()

    return recipe


def create_rating(rating, review_notes, favorite, external, recipe_id, user_id):
    """Create and return a new rating."""

    rating = Rating(rating=rating, review_notes=review_notes, favorite=favorite, external=external, recipe_id=recipe_id, user_id=user_id)

    db.session.add(rating)
    db.session.commit()

    return rating

def get_all_recipes():
    recipes = Recipe.query.all()

    return recipes

def get_recipes_by_search(search):
    
    #recipe_with_ingredient = db.session.query(Recipe).join(RecipeIngredient, RecipeIngredient.recipe_id == Recipe.recipe_id).join(Ingredient, Ingredient.ingredient == search)
    #result = recipe_with_ingredient.all()
    recipe_with_ingredient= db.session.query(Recipe.recipe_id, Recipe.title).join(RecipeIngredient).join(Ingredient).filter(Ingredient.ingredient == search).all()
    
    return recipe_with_ingredient

def get_user(email):
    return User.query.filter(User.email == email).first()

#def get_recipingredients():



    
  

   



if __name__ == '__main__':
    # since my server.py is not ready so for now commenting and using below
    #from server import app

    from flask import Flask
    app = Flask(__name__)

    connect_to_db(app)
