"""Server for Search Recipe app."""

from flask import (Flask, render_template, request, flash, session,
                   redirect, url_for)
from crud import create_user, create_dishtype, create_cuisine, create_diet, create_ingredient, create_recipeingredient, create_recipe, create_rating, get_all_recipes, get_recipes_by_search, get_recipes_by_recipe_id, get_user, get_user_by_userid, get_dishtype, get_diet, get_cuisine, get_ingredients, get_unit, get_recipe_from_db, get_recipeingredients_by_recipeid,get_ingredients_for_recipe, get_ingredient_by_name
from model import db, User, DishType, Cuisine, Diet, Ingredient, RecipeIngredient, Recipe, Rating, connect_to_db
import requests
import rapidapi
from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def homepage():
    """View homepage."""
    trivia = rapidapi.get_random_food_trivia()
    recipe = rapidapi.get_random_recipe()['recipes'][0]
    recipe1 = rapidapi.get_random_recipe()['recipes'][0]

    return render_template('homepage.html', trivia=trivia, recipe=recipe, recipe1=recipe1)


@app.route('/search/results')
def search_result():
    """View search form."""
    s = request.args.get('search')
   
    response_recipe_complex_json = rapidapi.get_recipe_complex_search(
        query=s, number=21)
    res = response_recipe_complex_json["results"]
    res_db = get_recipe_from_db(s)

    recipe_list = res_db + res
    n = len(recipe_list)
    if n > 0:
        return render_template('search-result.html', filtered_recipe=res_db + res, n=n)
    else:
        flash("No Recepies Found for  %s" % s)
        return redirect("/")    

@app.route('/recipe/details')
def get_recipe_details():
    """ view the details of the selected recipe either form db or API """
    
    rec_id = request.args['id']
    
    if rec_id.startswith("YR"):
        recipe_id_list = rec_id.split('-')
        recipe_id = recipe_id_list[1]

        recipe_details = get_recipes_by_recipe_id(recipe_id)
        db_rec_ings = get_ingredients_for_recipe(recipe_id)
        ingredients_list_image = []
        for db_rec_ing in db_rec_ings:
            ing_list = {}
            ing_list['name'] = db_rec_ing[1]
            ing_list['image'] = "/static/img/ing.jpg"
            ing_list['amount'] = str(db_rec_ing[0]) + " " + db_rec_ing[2]
            ingredients_list_image.append(ing_list)
            n = len(ingredients_list_image)

    else:
        recipe_id = request.args['id']

        recipe_details = rapidapi.get_recipe_details_by_id(recipe_id)
        recipe_nutritions = rapidapi.get_recipe_nutriinfo(recipe_id)

        recipe_details['calories'] = recipe_nutritions['calories']
        recipe_details['carbs'] = recipe_nutritions['carbs']
        recipe_details['fat'] = recipe_nutritions['fat']
        recipe_details['protein'] = recipe_nutritions['protein']
        recipe_details['bad_nutri'] = recipe_nutritions['bad'][:7]
        recipe_details['good_nutri'] = recipe_nutritions['good'][:7]
        recipe_details['cookingMinutes'] = recipe_details.get('cookingMinutes', None)
        recipe_details['preparationMinutes'] = recipe_details.get('preparationMinutes', None)
        
        if not recipe_details['diets']:
            recipe_details['diets'] = "None "
         
        else:
            recipe_details['diets'] = recipe_details['diets'][0]
       
  
        if len(recipe_details['cuisines']) <= 0:
            recipe_details['cuisines'] = None
        if len(recipe_details['dishTypes']) <= 0:
            recipe_details['dishTypes'] = None

        rec_ing = rapidapi.get_ingredients_list_of_recipe(recipe_id)
        ingredients_list_image = []
        for ing in rec_ing['ingredients']:
            ing_list = {}
            ing_list['name'] = ing['name']
            ing_list['image'] = "https://spoonacular.com/cdn/ingredients_100x100/{0}".format(
                ing['image'])
            ing_list['amount'] = str("{:.2f}".format(
                ing['amount']['us']['value'])) + " " + ing['amount']['us']['unit']
            ingredients_list_image.append(ing_list)
            n = len(ingredients_list_image)

    if recipe_details['instructions'] == "<p>Instructions</p>" or recipe_details['instructions'] == None:
        recipe_details['instructions'] = recipe_details['summary']

    recipe_details['hidden_instructions'] = recipe_details['instructions']

    # lines = recipe_details['instructions'].split(".")
    # # pop the end blank line from list
    # lines.pop(-1)
    # recipe_details['instructions'] = lines

    show_fav_link = True
    if "user_id" in session:
        user_id = session.get('user_id')
        check_rating = Rating.query.filter(Rating.user_id == user_id).filter(
            Rating.recipe_id == recipe_id).all()

        if check_rating:
            show_fav_link = False
            recipe_details['review_notes'] = check_rating[0].review_notes

    session['redirect_recipe_id'] = recipe_id
    return render_template('recipe-details.html', recipe=recipe_details, show_fav_link=show_fav_link, ings=ingredients_list_image, n=n)


@app.route('/signin', methods=["GET", "POST"])
def sign_in():
    """ Loging to the page """
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user = get_user(email)
        # if password matches and is in db
        if user and password == user.password:
            session["user_id"] = user.user_id
            session["fname"] = user.fname
            flash("Logged in as %s" % user.fname)
            if 'redirect_recipe_id' in session:
                redirect_recipe_id = int(session['redirect_recipe_id'])
                #session['redirect_recipe_id'].clear()
                if isinstance(redirect_recipe_id, int):
                    return redirect(f'/recipe/details?id={redirect_recipe_id}')
            else:
                return redirect('/')

        # email is in db but typed wrong pwd
        elif user and email == user.email:
            flash("Please Check Your Password")
            return redirect('/signin')

        # if user not in db to signup
        else:
            flash("PLEASE SIGNUP")
            return redirect('/signup')
    else:
        return render_template('login.html')


@app.route('/logout')
def user_logout():
    """ Logout """
    session.clear()
    flash("Logged Out")
    return redirect("/")


@app.route('/signup', methods=["GET", "POST"])
def sign_up():
    """ If new user then signup  """

    if request.method == "GET":
        return render_template("signup.html")

    if request.method == "POST":
        email = request.form.get("email")
        firstname = request.form.get("firstname")
        lastname = request.form.get("lastname")
        mobileno = request.form.get("mobile-no")
        password = request.form.get("password")
        user = get_user(email)
        if user:
            flash("Check your email and password")
            return redirect('/signin')
        else:
            create_user(firstname, lastname, email, password, mobileno)
            return redirect('/signin')


@app.route('/my-fav')
def favorite():
    """View favorites page of user."""

    if 'user_id' in session:
        user_id = session.get('user_id')
        ratings = Rating.query.filter(Rating.user_id == user_id).all()
        fav_list = []
        for rating in ratings:
            fav_dict = {}
            fav_dict["recipe_id"] = rating.recipe_id
            if rating.external:
                fav_dict["title"] = rating.title_ext
                # to get the first 250 characters
                fav_dict["description"] = rating.description_ext[:250]

            else:
                recipes = Recipe.query.filter(
                    Recipe.recipe_id == rating.recipe_id).all()
                fav_dict["title"] = recipes.title
                fav_dict["description"] = recipes.description
            fav_list.append(fav_dict)

        recipes = db.session.query(Recipe).filter(
            Recipe.user_id == user_id).order_by(Recipe.recipe_id.desc()).all()

        my_recipe_list = []
        for recipe in recipes:
            rec_dict = {}
            rec_dict["recipe_id"] = f"YR-{recipe.recipe_id}"
            rec_dict["title"] = recipe.title
            rec_dict["description"] = recipe.description
            rec_dict["instructions"] = recipe.instructions
            my_recipe_list.append(rec_dict)

        return render_template('my-favorites.html', fav_list=fav_list, my_recipe_list=my_recipe_list)
    else:
        flash("Login to see your favorites")
        return redirect("/signin")

@app.route('/submit-your-recipe', methods=["GET","POST"])
def submit_your_recipe():
    """ submit the created recipe """
    if request.method == 'POST':
    
        if 'user_id' in session:

            
            user_id = session.get('user_id')
            recipe_title = request.form.get("recipe-title")
            recipe_instructions = request.form.get("instructions")
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
            url = ""

            if request.form.get("ingrow") is None:
                ingrow = 0
                flash("enter at least one ingredient")
            else:
                ingrow = request.form.get("ingrow")

            ingredients = []
            i = 1

            while i <= int(ingrow):
                ingredient_row = request.form.get(f"ingrow{i}")
                # ingredient_tuple = tuple(map(str, ingredient_row.split(',')))
                # new recipe ingredient rows from html[['1', '3', '3', 'papaya'], ['2', '3', '3'], ['1', '3', '3', 'test ingredient']]
                # ['1', '3', '3', 'papaya']
                # ingredient_list[0] = ingredient_id, ingredient_list[1] = unit,ingredient_list[2] = quantity, if other ingredient_list[3] = name,
                print("######################### ingrow", ingredient_row)
                if ingredient_row: 
                    ingredient_list = ingredient_row.split(',')
                    ingredients.append(ingredient_list)
                i += 1

            new_recipe = create_recipe(recipe_title, recipe_description, prep_time,
                                    cook_time, dishtype, cuisine, diet, recipe_instructions, url, user_id)
            new_recipe_id = new_recipe.recipe_id
            if new_recipe_id:
                for index, ingredient_list in enumerate(ingredients):
                    if ingredient_list[0] == "1":
                        check_new_ing = get_ingredient_by_name(ingredient=ingredient_list[3])

                        if check_new_ing:
                            ingredient_to_insert = check_new_ing.ingredient_id
                        else:
                            new_ingredient = create_ingredient(
                                ingredient_list[3], ingredient_list[1])
                            ingredient_to_insert = new_ingredient.ingredient_id
    
                    else:
                        ingredient_to_insert = int(ingredient_list[0])

                    create_recipeingredient(
                        ingredient_to_insert, new_recipe_id, ingredient_list[2])

            return redirect('/my-fav')
    else:
        if 'user_id' in session:
            user_id = session.get('user_id')
            diet_picklist = get_diet()
            dish_picklist = get_cuisine()
            cuisine_picklist = get_dishtype()
            ing_picklist = get_ingredients()
            unit_picklist = get_unit()
            return render_template('add-your-recipe.html', diet_picklist=diet_picklist, dish_picklist=dish_picklist, cuisine_picklist=cuisine_picklist, ing_picklist=ing_picklist, unit_picklist=unit_picklist)

        else:
            flash("Please login to create/add your recipe")
            return redirect('/signin')



@app.route('/add-to-favorite', methods=['POST'])
def add_to_your_favorite():
    """ If a recipe is intersting add to user's favorite page"""
    if 'user_id' in session:
        user_id = session.get('user_id')
        recipe_id = request.form.get("recipe-id")
        recipe_title = request.form.get("recipe-title")
        recipe_instructions = request.form.get("recipe-instructions")
        review_notes = request.form.get("review-notes")
        if Recipe.query.get(recipe_id) is None:
            external = True
        favorite = True
        check_rating = Rating.query.filter(Rating.user_id == user_id).filter(
            Rating.recipe_id == recipe_id).filter(Rating.external == external).all()
        if not check_rating:
            create_rating(1, review_notes, favorite, external,
                          recipe_id, recipe_title, recipe_instructions, user_id)
            
            flash("Recipe added to favorites")

        return redirect(f'/recipe/details?id={recipe_id}')
    else:
        flash("Please Login before you add to your favorite")
        return redirect("/signin")


@app.errorhandler(404)
def page_not_found(error):
    """ Handling page not found"""
    return render_template('404.html')

@app.errorhandler(500)
def page_not_found(error):
    """ handling internal server error"""
    return render_template('500.html')

@app.errorhandler(Exception)
def page_not_found(error):
    """ handling internal server error"""
    app.logger.exception(error)
    return render_template('500.html')


if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)
