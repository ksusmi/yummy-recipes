"""Server for movie ratings app."""

from flask import (Flask, render_template, request, flash, session,
                   redirect)
# from model import connect_to_db
# import crud
from crud import create_user, create_dishtype, create_cuisine, create_diet, create_ingredient, create_recipeingredient, create_recipe, create_rating, get_allrecipes
from model import db, User, DishType, Cuisine, Diet, Ingredient, RecipeIngredient, Recipe, Rating, connect_to_db

#  from jinja2 called StrictUndefined. 
#  You’ll use it to configure a Jinja2 setting to make it throw errors for undefined variables
from jinja2 import StrictUndefined

app = Flask(__name__)
# for encryption
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

# Replace this with routes and view functions!
@app.route('/')
def homepage():
    """View homepage."""

    return render_template('homepage1.html')

@app.route('/search/result')
def search_result():
    """View searchpage."""
    



    return render_template('searchResult.html')

@app.route('/search')
def search():
    """View searchpage."""
    all_recipes = get_allrecipes()



    return render_template('homepage1.html', all_recipes=all_recipes)

@app.route('/login')
def login():
    """View registration/login page."""

    return render_template('login.html')

@app.route('/favorite')
def favorite():
    """View favorites page of user."""

    return render_template('favorite.html')


# connect to your database before app.run gets called. 
# If you don’t do this, Flask won’t be able to access your database!

if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)
