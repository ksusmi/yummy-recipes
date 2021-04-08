"""Server for movie ratings app."""

from flask import (Flask, render_template, request, flash, session,
                   redirect)
# from model import connect_to_db
# import crud
from crud import create_user, create_dishtype, create_cuisine, create_diet, create_ingredient, create_recipeingredient, create_recipe, create_rating
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

    return render_template('homepage.html')


# connect to your database before app.run gets called. 
# If you don’t do this, Flask won’t be able to access your database!

if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)
