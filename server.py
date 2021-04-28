"""Server for movie ratings app."""


#from flask_bootstrap import Bootstrap
#from flask_wtf import Flaskform
#from wtforms import StringField, PasswordField, BooleanField
#from wtforms.validators import InputRequired, Email, Length

from flask import (Flask, render_template, request, flash, session,
                   redirect, url_for)
from crud import create_user, create_dishtype, create_cuisine, create_diet, create_ingredient, create_recipeingredient, create_recipe, create_rating, get_all_recipes,get_recipes_by_search, get_user, get_user_by_userid,get_dishtype, get_diet, get_cuisine, get_ingredients, get_unit
from model import db, User, DishType, Cuisine, Diet, Ingredient, RecipeIngredient, Recipe, Rating, connect_to_db
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
    print("################ Search from /search #########", search)

    return redirect('/search/results')

@app.route('/search/results')
def search_result():
    """View searchpage."""
    if "user_id" in session:

        s = session['search']
        #response_json = rapidapi.get_recipe_by_ingredients(s)
        response_recipe_complex_json = rapidapi.get_recipe_complex_search(query=s, number=10)
        res = response_recipe_complex_json["results"]
        #print("#############################   Complex Search##############", response_recipe_complex_json)

        # print("search string******************" + s)
        # res =[]
        # for data in response_json:
        #     ot={}         
        #     ot['id'] = data['id']
        #     ot['title'] = data['title']
        #     ot['image'] = data['image']
        #     res.append(ot)
        # return render_template('search-result.html', filtered_recipe = res)
        
        recipe_from_db = Recipe.query.filter(Recipe.instructions.like(s)).all()
        print("################# recipe details from db ##########",recipe_from_db )

        return render_template('search-result.html', filtered_recipe = res)

    else:
        flash ("Please Login before you start your search")
        return redirect ("/login")

@app.route('/recipe/details')
def get_recipe_details():
    user_id = session.get('user_id')
    #s = session['search']
    recipe_id = request.args['id']
    
    res1=[]
    ot1 = {}

    recipe_details= rapidapi.get_recipe_details_by_id(recipe_id)

    print("**********************************\n ****************************")
    print(recipe_id)
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

    ot1['calories'] = recipe_nutritions['calories']
    ot1['carbs'] = recipe_nutritions['carbs']
    ot1['fat'] = recipe_nutritions['fat']
    ot1['protein'] = recipe_nutritions['protein']
    res1.append(ot1)

    check_rating = Rating.query.filter(Rating.user_id == user_id).filter( Rating.recipe_id == recipe_id).all()
    if check_rating:
        show_fav_link = False
    else:
        show_fav_link = True
 
    return render_template('recipe-details.html', recipe=recipe_details, res = res1, cuisines = cuisines,dishType=dishType, diets=diets, show_fav_link = show_fav_link)


@app.route('/login')
def login():
    """View registration/login page."""

    return render_template('login.html')


@app.route('/signin', methods = ["POST"])
def sign_in():
    email = request.form.get("email")
    password = request.form.get("password")
    user = get_user(email)
    print (email, password)
    # if password matches and is in db
    if user and password == user.password:
        session["user_id"] = user.user_id
        session["fname"] = user.fname
        print(session, 'SESSION!!!!!!')
        flash("Logged in as %s" % user.fname)
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
    """ Logout """  
  
    #del session["user_id"]
    session.clear()
    flash ("Logged Out")
    return redirect ("/")


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


@app.route('/my-fav')
def favorite():
    """View favorites page of user."""
    if 'user_id' in session:
        user_id = session.get('user_id')
        #User.query.filter(User.user_id == user_id).join
        #fav_recipes_of_user= db.session.query(Recipe.recipe_id, Recipe.title, Recipe.instructions).join(RecipeIngredient).join(Ingredient).filter(User.user_id == user_id).all()
        ratings = Rating.query.filter(Rating.user_id == user_id).all()
        fav_list=[]
        for rating in ratings:
            fav_dict={}
            fav_dict["recipe_id"] = rating.recipe_id
            if rating.external:
                fav_dict["title"] = rating.title_ext
                fav_dict["description"] = rating.description_ext

            else:
                recipes = Recipe.query.filter(Recipe.recipe_id == rating.recipe_id).all()
                print("##########################", rcipes)
                fav_dict["title"] = recipes.title
                fav_dict["description"] = recipes.description
            fav_list.append(fav_dict)
        #recipes = Recipe.query(Recipe.description, Recipe.title).filter(Recipe.recipe_id == rating.recipe_id).all()
        #recipes = Recipe.query.filter(Recipe.user_id == user_id).all()
        recipes = db.session.query(Recipe).filter(Recipe.user_id == user_id).order_by(Recipe.recipe_id.desc()).all()
        print("########## My Recipes sorted ##########", recipes)
        my_recipe_list =[]
        for recipe in recipes:
            rec_dict={}
            rec_dict["title"] = recipe.title
            rec_dict["description"] = recipe.description
            rec_dict["instructions"] = recipe.instructions
            my_recipe_list.append(rec_dict)
        
    return render_template('my-favorites.html', fav_list = fav_list, my_recipe_list=my_recipe_list)

@app.route('/add-your-recipe')
def add_your_recipe():
    if 'user_id' in session:
        user_id = session.get('user_id')
        diet_picklist = get_diet()
        dish_picklist = get_cuisine()
        cuisine_picklist = get_dishtype()
        ing_picklist = get_ingredients()
        unit_picklist = get_unit()
         
    return render_template('add-your-recipe.html',diet_picklist=diet_picklist, dish_picklist=dish_picklist, cuisine_picklist=cuisine_picklist, ing_picklist=ing_picklist, unit_picklist=unit_picklist)
 

@app.route('/submit-your-recipe', methods = ["POST"])
def submit_your_recipe():
    if 'user_id' in session:
        print("request data - " , request.form)
        user_id = session.get('user_id')
        recipe_title = request.form.get("recipe-title")
        recipe_instructions = request.form.get("instructions")
        #prep_time = request.form.get("prep-time")
        if request.form.get("preptime") == "":
            prep_time = 0
        else:
            prep_time = request.form.get("preptime")

        if request.form.get("cooktime") == "":
            cook_time = 0
        else:
            cook_time = request.form.get("cooktime")

        recipe_description = request.form.get("description")

        if request.form.get("diet") == "":
            diet = 1
        else:
            diet = request.form.get("diet")

        if request.form.get("cuisine") == "":
            cuisine = 1
        else:
            cuisine = request.form.get("cuisine")

        if request.form.get("dishtype") == "":
            dishtype = 1
        else:
            dishtype = request.form.get("dishtype")

        # ingredients = request.form.get("ingredients")
        url = ""
        
        if request.form.get("ingrow") is None:
            ingrow = 0
            #Raise message 
            flash("enter at least one ingredient")
        else:
            ingrow = request.form.get("ingrow")

        ingredients = []
        i = 1
        print("######## ingredient row count", ingrow)

        while i <= int(ingrow):
            ingredient_row = request.form.get(f"ingrow{i}")
            # ingredient_tuple = tuple(map(str, ingredient_row.split(',')))
            # new recipe ingredient rows from html[['1', '3', '3', 'papaya'], ['2', '3', '3'], ['1', '3', '3', 'test ingredient']]
            # ['1', '3', '3', 'papaya']
            # ingredient_list[0] = ingredient_id, ingredient_list[1] = unit,ingredient_list[2] = quantity, if other ingredient_list[3] = name,
            ingredient_list = ingredient_row.split(',')
            ingredients.append(ingredient_list)
            i += 1
        print("######## ingredient table html", ingredients)
        
        new_recipe = create_recipe(recipe_title, recipe_description, prep_time, cook_time, dishtype, cuisine, diet, recipe_instructions, url, user_id)    
        new_recipe_id = new_recipe.recipe_id
        if new_recipe_id:
            for index,ingredient_list in enumerate(ingredients):
                print("ingredient_list - ", ingredient_list)
                if ingredient_list[0] == "1":
                    #check_new_ing = Ingredient.query().filter(Ingredient.ingredient == ingredient_list[3]).first() 
                    check_new_ing = db.session.query(Ingredient).filter_by(ingredient = ingredient_list[3]).scalar()
                    print("############### new ingredient check ##################",check_new_ing)
                    if check_new_ing:
                        ingredient_to_insert = check_new_ing.ingredient_id
                    else:
                        new_ingredient = create_ingredient(ingredient_list[3], ingredient_list[1])
                        ingredient_to_insert = new_ingredient.ingredient_id
                        print("############### New Ingredient Added ################", new_ingredient)
                        #print("New Ingredient Added", Ingredient.query.filter(Ingredient.ingredient_id == ingredient_to_insert).all())                
                else:
                    ingredient_to_insert = int(ingredient_list[0])
                        
                create_recipeingredient(ingredient_to_insert, new_recipe_id, ingredient_list[2])

        print("##############  Recipe Created #################", Recipe.query.filter(Recipe.recipe_id == new_recipe_id).all())
        print("##############  Recipe Ingredients Created #################",RecipeIngredient.query.filter(RecipeIngredient.recipe_id == new_recipe_id).all())
        
        return redirect('/my-fav')


@app.route('/add-to-favorite', methods=['POST'])
def add_to_your_favorite():
    if 'user_id' in session:
        user_id = session.get('user_id')
        recipe_id = request.form.get("recipe-id")
        recipe_title = request.form.get("recipe-title")
        recipe_instructions = request.form.get("recipe-instructions")
        review_notes= request.form.get("review-notes")
        #recipe = Recipe.query.get(recipe_id)
        if Recipe.query.get(recipe_id) is None:
            external = True
            #external = request.form.get("external")
        favorite = True
        check_rating = Rating.query.filter(Rating.user_id == user_id).filter( Rating.recipe_id == recipe_id).filter(Rating.external == external).all()
        if not  check_rating:
            create_rating(1, review_notes, favorite, external, recipe_id, recipe_title, recipe_instructions, user_id)
            print("************ Successfully added" )
            flash ("Recipe added to favorites")
        #review_notes.clear()
        
        return redirect(f'/recipe/details?id={recipe_id}')


        #check_rating = Rating.query.filter(Rating.user_id == user_id).filter( Rating.recipe_id == recipe_id).filter(Rating.external == external).first()

# connect to your database before app.run gets called. 
# If you don’t do this, Flask won’t be able to access your database!

if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)
