"""Server for movie ratings app."""

from flask import (Flask, render_template, request, flash, session,
                   redirect)

#from flask_bootstrap import Bootstrap
#from flask_wtf import Flaskform
#from wtforms import StringField, PasswordField, BooleanField
#from wtforms.validators import InputRequired, Email, Length
# from model import connect_to_db
# import crud
from crud import create_user, create_dishtype, create_cuisine, create_diet, create_ingredient, create_recipeingredient, create_recipe, create_rating, get_all_recipes,get_recipes_by_search, get_user, get_user_by_userid
from model import db, User, DishType, Cuisine, Diet, Ingredient, RecipeIngredient, Recipe, Rating, connect_to_db
#from api import SpoonacularApi
import requests
import rapidapi

#  from jinja2 called StrictUndefined. 
#  You’ll use it to configure a Jinja2 setting to make it throw errors for undefined variables
from jinja2 import StrictUndefined

app = Flask(__name__)
# for encryption
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

@app.route('/')
def homepage():
    """View homepage."""

    return render_template('homepage.html')

@app.route('/search')
def search():
    """get the search value from homepage and store in session."""
    search = request.args.get('search')
    session['search'] = search

    return redirect('/search/results')

@app.route('/search/results')
def search_result():
    """View searchpage."""
    if "user_id" in session:

        s = session['search']
        response_json = rapidapi.get_recipe_by_ingredients(s)
        print("search string******************" + s)
        res =[]
        for data in response_json:
            ot={}         
            ot['id'] = data['id']
            ot['title'] = data['title']
            ot['image'] = data['image']
            res.append(ot)
        return render_template('searchResult.html', filtered_recipe = res)

    else:
        flash ("Please Login before you start your search")
        return redirect ("/login")

@app.route('/recipe/details')
def get_recipe_details():
    s = session['search']
    recipe_id = request.args['id']
    
    res1=[]
    ot1 = {}

    recipe_details= rapidapi.get_recipe_details_by_id(recipe_id)

    print("**********************************\n ****************************")
    #print(recipe_details)
    print("**********************************\n ****************************")

    cuisines= recipe_details["cuisines"]
    dishType = recipe_details["dishTypes"]
    diets = recipe_details["diets"]

    ot1['vegetarian'] = recipe_details['vegetarian']
    ot1['vegan'] =recipe_details['vegan']
    ot1['glutenFree'] =recipe_details['glutenFree']
    ot1['dairyFree'] = recipe_details['dairyFree']
    ot1['veryHealthy'] =recipe_details['veryHealthy']
    ot1['pricePerServing'] =recipe_details['pricePerServing']
    ot1['readyInMinutes'] = recipe_details['readyInMinutes']

    recipe_nutritions = rapidapi.get_recipe_nutriinfo(recipe_id)
    print ("*******************************")
    print (recipe_nutritions)

    ot1['calories'] = recipe_nutritions['calories']
    ot1['carbs'] = recipe_nutritions['carbs']
    ot1['fat'] = recipe_nutritions['fat']
    ot1['protein'] = recipe_nutritions['protein']
    print (recipe_nutritions)
    res1.append(ot1)
    
    return render_template('recipedetails.html', recipe=recipe_details, res = res1, cuisines = cuisines,dishType=dishType, diets=diets,)


@app.route('/login')
def login():
    """View registration/login page."""
    
    return render_template('login.html')


@app.route('/signin', methods = ["POST"])
def sign_in():
    print(request.origin)
    email = request.form.get("email")
    password = request.form.get("password")
    user = get_user(email)
    # if password matches and is in db
    if user and password == user.password:
        # I have to set user_id to session only here 
        # every where else i have to be checking
        session["user_id"] = user.user_id
        session["fname"] = user.fname
        print(session, 'SESSION!!!!!!')
        flash("Logged in as %s" % user.user_id)
        return redirect('/')

    # email is in db but typed wrong pwd
    elif user and email == user.email:
        flash ("Please Check Your Password")
        return redirect('/login')
    
    # if user not in db to signup
    else:
       flash ("PLEASE SIGNUP") 
       return redirect('/login')

@app.route('/logout')
def user_logout():  

    user_id = session.get('user_id')
    if user_id:
        user = get_user_by_userid(user_id)
        session.clear()
        return render_template("logout.html", user=user)
    else:
        return redirect ("/login")

    #logout keys to remove from session    
    # logout_keys_to_remove = ["fname", "user_id"]
    # for key in logout_keys_to_remove:
    #    session.pop(key,None)
    # flash ("You logged in as %s" % session['fname'])
    # flash("Thank You for choosing Yummy Recipe Website")

    # return render_template("logout.html")


# @app.route('/get-name')
# def get_name():
#     """Get name from homepage form and store name in session."""

#     name = request.args.get('name')
#     session['name'] = name

# user = User.query.get(session['user_id'])
# return render_template('page.html', user=user)
    

@app.route('/signup', methods = ["GET", "POST"])
def sign_up():
    if request.method == "GET":
        return render_template("signup.html")
    if request.method == "POST":
        email = request.form.get("email")
        firstname = request.form.get("firstname")
        lastname = request.form.get("lastname")
        mobileno = request.form.get("mobile-no")
        password = request.form.get("password")
        create_user(firstname, lastname, email, password, mobileno)
        return redirect ('/login')


@app.route('/favorite')
def favorite():
    """View favorites page of user."""

    return render_template('favorite.html')

@app.route('/add/yourrecipe')
def add_your_recipe():
    return render_template('addyourrecipe.html')

# connect to your database before app.run gets called. 
# If you don’t do this, Flask won’t be able to access your database!

if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)
