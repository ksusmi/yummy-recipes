"""CRUD operations."""

from model import db, User, DishType, Cuisine, Diet, Ingredient, RecipeIngredient, Recipe, Rating, connect_to_db
#from server import app


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

def create_recipe(title, description, prep_time, cook_time, dishtype_id, cuisine_id,diet_id, instructions,url, user_id):
    """Create and return the recipe created """

    recipe = Recipe(title = title, description= description, prep_time= prep_time, cook_time=cook_time, dishtype_id= dishtype_id, cuisine_id=cuisine_id, diet_id=diet_id, instructions= instructions,url=url,user_id=user_id)

    db.session.add(recipe)
    db.session.commit()

    return recipe


def create_rating(rating, review_notes, favorite, external, recipe_id, title_ext, description_ext, user_id):
    """Create and return a new rating."""

    rating = Rating(rating=rating, review_notes=review_notes, favorite=favorite, external=external, recipe_id=recipe_id, title_ext=title_ext, description_ext=description_ext, user_id=user_id)

    db.session.add(rating)
    db.session.commit()

    return rating



def get_all_recipes():
    recipes = Recipe.query.all()

    return recipes

def get_recipes_by_search(search):
    
    recipe_with_ingredient= db.session.query(Recipe.recipe_id, Recipe.title).join(RecipeIngredient).join(Ingredient).filter(Ingredient.ingredient == search).all()
    
    return recipe_with_ingredient

def get_recipes_by_recipe_id(recipe_id):
    #recipes = Recipe.query(Recipe.instructions, Recipe.title).filter(Recipe.recipe_id == recipe_id).all()
    #recipe_db = Recipe.query.filter(Recipe.recipe_id == recipe_id).all()
    recipe_dbs = db.session.query(Recipe, DishType.dishtype_name,Cuisine.cuisine_name,Diet.diet_name).join(DishType).join(Cuisine).join(Diet).filter(Recipe.recipe_id == recipe_id).all()
    print ("################# get recipe from my db ######### ", recipe_dbs)
    for recipe_db in recipe_dbs:
        recipe_details = {}
        recipe_details["id"] = recipe_db[0].recipe_id
        recipe_details["title"] = recipe_db[0].title
        recipe_details["instructions"] = recipe_db[0].instructions
        recipe_details["image"] = "../static/img/generic_recipe.png"
        recipe_details["dishTypes"] = recipe_db[1]
        recipe_details["cuisines"] = recipe_db[2]
        recipe_details["diets"] = recipe_db[3]
        recipe_details["inregdientsWidget"] = " "
        recipe_details["equipmentWidget"] = " "
        recipe_details["calories"] = None
        recipe_details["carbs"] = None
        recipe_details["fat"] = None
        recipe_details["protein"] = None
        recipe_details["vegan"] = None
        recipe_details["vegetarian"] = None
        recipe_details["glutenFree"] = None
        recipe_details["veryHealthy"] = None
        recipe_details["pricePerServing"] = None
        recipe_details["readyInMinutes"] = None
        recipe_details["dairyFree"] = None
    return recipe_details

def get_recipe_by_desc(user_id):
    recipes = db.session.query(Recipe).filter(Recipe.user_id == user_id).order_by(Recipe.recipe_id.desc()).all()
    return recipes


def get_recipe_by_user_id(user_id):
    recipes = Recipe.query.filter(Recipe.user_id == user_id).all()
    return recipes

def get_user(email):
    return User.query.filter(User.email == email).first()

def get_user_by_userid(user_id):
    return User.query.filter(User.user_id == user_id).first()

def get_user_fav_recipes(user_id):
    fav_recipes_of_user= db.session.query(Recipe.recipe_id, Recipe.title, Recipe.instructions).join(RecipeIngredient).join(Ingredient).filter(User.user_id == user_id).all()
    return fav_recipes_of_user

# def get():
#     check_rating = Rating.query.filter(Rating.user_id == user_id).filter( Rating.recipe_id == recipe_id).filter(Rating.external == external).first()


def get_dishtype():
    return dishtype_list_to_dict(DishType.query.all())

def get_diet():
    return diet_list_to_dict(Diet.query.all())

def get_cuisine():
    return cuisine_list_to_dict(Cuisine.query.all())

def get_ingredients():
    return ingredient_list_to_dict(Ingredient.query.all())

def get_unit():
    return unit_list_to_dict(Ingredient.query.all())



def get_recipe_from_db(search):
    list_obj = Recipe.query.filter(Recipe.title.ilike(search)).all()
    print ("******************** list_obj **************", list_obj)
    res_db_list = []
    for obj1 in list_obj:
        dict_obj={}
        dict_obj["id"] = f"YR-{obj1.recipe_id}"
        dict_obj["title"] = obj1.title
        dict_obj["instructions"] = obj1.instructions
        dict_obj["image"] = "../static/img/generic_recipe.png"
        res_db_list.append(dict_obj)
    return res_db_list

def diet_list_to_dict(list_obj):
    dict_obj={}
    for obj1 in list_obj:
        dict_obj[obj1.diet_id] = obj1.diet_name
    return dict_obj

def dishtype_list_to_dict(list_obj):
    dict_obj={}
    for obj1 in list_obj:
        dict_obj[obj1.dishtype_id] = obj1.dishtype_name
    return dict_obj

def cuisine_list_to_dict(list_obj):
    dict_obj={}
    for obj1 in list_obj:
        dict_obj[obj1.cuisine_id] = obj1.cuisine_name
    return dict_obj

def ingredient_list_to_dict(list_obj):
    dict_obj={}
    for obj1 in list_obj:
        dict_obj[obj1.ingredient_id] = obj1.ingredient
    return dict_obj 

def unit_list_to_dict(list_obj):
    dict_obj={}
    for obj1 in list_obj:
        dict_obj[obj1.ingredient_id] = obj1.unit
    return dict_obj


def search_by_ingredient():
        if "user_id" in session:

            s = session['search']
            response_json = rapidapi.get_recipe_by_ingredients(s)
            recipe_from_db = Recipe.query.filter(Recipe.title.ilike(s)).all()
            print("search string******************" + s)
            res =[]
            for data in response_json:
                ot={}         
                ot['id'] = data['id']
                ot['title'] = data['title']
                ot['image'] = data['image']
                res.append(ot)
            return render_template('search-result.html', filtered_recipe = res)
        
            recipe_from_db = Recipe.query.filter(Recipe.title.ilike(s)).all()
            print("################# recipe details from db ##########",recipe_from_db )
            return render_template('search-result.html', filtered_recipe = res)

        else:
            flash ("Please Login before you start your search")
            return redirect ("/login")





if __name__ == '__main__':
    # since my server.py is not ready so for now commenting and using below
    from flask import Flask
    app = Flask(__name__)
    #server is ready
    #from server import app
    connect_to_db(app)
