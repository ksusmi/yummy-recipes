from crud import create_user, create_dishtype, create_cuisine, create_diet, create_ingredient, create_recipeingredient, create_recipe, create_rating
from model import db, User, DishType, Cuisine, Diet, Ingredient, RecipeIngredient, Recipe, Rating, connect_to_db
from random import choice, randint
import os
def create_example_data():
    # create users
    user_in_db = [] 
    for n in range(10):
        email = f'user{n}@test.com'  
        password = f'test{n}'
        mobile_no= f'{n}{n}{n}{n}{n}'
        fname = f'jill{n}'
        lname = f'jam{n}'
        db_user = create_user(fname, lname, email, password, mobile_no)
        user_in_db.append(db_user)

    # create dishtypes
    mydishtype = ['','snack', 'appetizer', 'soup', 'starter', 'entree', 'dessert', 'drink', 'beverage', 'side', 'cocktail']
    dish_in_db = []

    for dish in mydishtype:
        db_dishtype = create_dishtype(dish)
        dish_in_db.append(db_dishtype)
    
    # create cuisines
    mycusine = ['','american', 'indian', 'italian', 'mexican', 'chinese', 'vietname', 'korean', 'japanese', 'mediterranean', 'thai' ]
    cuisine_in_db = []
    for cuisine in mycusine:
        db_cuisine = create_cuisine(cuisine)
        cuisine_in_db.append(db_cuisine)
    
    # create diets
    mydiet = ['','vegan', 'vegetarian', 'gluteen free', 'diary free', 'mediterranen', 'pescatarian', 'vegan', 'vegan', 'vegan', 'vegan']
    diet_in_db=[]
    for diet in mydiet:
        db_diet = create_diet(diet)
        diet_in_db.append(db_diet)

    # create ingredients
    mying = ['other','potato','pancake mix', 'flour', 'chilli powder', 'cheese' ]
    myunit= ['each', 'cup', 'cup', 'tbsp', 'oz']
    ing_in_db = []
    i=0
    while i < 5:
        db_ing = create_ingredient(mying[i], myunit[i])
        i +=1
        ing_in_db.append(db_ing)
    
    # create recipes
    rec_title = ['pancake', 'cupcake', 'omlete', 'fried rice', 'sandwitch','cheese burger', 'cake', 'tomato soup', 'falooda', 'mango moose']
    rec_des=['pancake', 'cupcake', 'omlete', 'fried rice', 'sandwitch','cheese burger', 'cake', 'tomato soup_desc', 'falooda_desc', 'mango moose_desc']
    rec_inst = "instructions"
    rec_url = " "
    rec_in_db =[]
    i=0
    
    while i < 10:
        db_recipe = create_recipe( rec_title[i], f'{rec_des[i]} _desc', i*2, i*4, dish_in_db[i].dishtype_id, cuisine_in_db[i].cuisine_id, diet_in_db[i].diet_id, f'{rec_inst} _ {i}', rec_url, user_in_db[i].user_id)
        rec_in_db.append(db_recipe)
        i +=1
    
    # create recipe ingredients
    i = 0
    while i < 10:

        for r in range(randint(1, 5)):
            q = randint (1, 5)

            create_recipeingredient(ing_in_db[r].ingredient_id,rec_in_db[i].recipe_id,q)
        i += 1
    
    db.session.commit()

if __name__ == "__main__":
    from flask import Flask
    app = Flask(__name__)
    os.system('dropdb testdb')
    os.system('createdb testdb')
    connect_to_db(app, "postgresql:///testdb")
    db.create_all()
    create_example_data()