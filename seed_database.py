"""Script to seed database."""
# OS - This is a module from Python’s standard library. 
# It contains code related to working with your computer’s operating system.

import os

# crud, model, and server
# These are all files that you wrote (or will write) — crud.py, model.py, and server.py
from crud import create_user, create_dishtype, create_cuisine, create_diet, create_ingredient, create_recipeingredient, create_recipe, create_rating
from model import db, User, DishType, Cuisine, Diet, Ingredient, RecipeIngredient, Recipe, Rating, connect_to_db
#import server

# choice and randit
# choice is a function that takes in a list and returns a random element in the list. randint will return a random number within a certain range. 
# You’ll use both to generate fake users and ratings
from random import choice, randint

os.system('dropdb searchrecipe')
os.system('createdb searchrecipe')

#model.connect_to_db(server.app)
# ????? since my server.py is not ready
from flask import Flask
app = Flask(__name__)

connect_to_db(app)
db.create_all()



# Create 10 users;
user_in_db = [] 
for n in range(10):
    email = f'user{n}@test.com'  # Voila! A unique email!
    password = f'test{n}'
    mobile_no= f'{n}{n}{n}{n}{n}'
    fname = f'jill{n}'
    lname = f'jam{n}'

        # TODO: create a user here
    db_user = create_user(fname, lname, email, password, mobile_no)
    user_in_db.append(db_user)


# dishtype = create_dishtype('snack')
mydishtype = ['snack', 'appetizer', 'soup', 'starter', 'entree', 'dessert', 'drink', 'beverage', 'side', 'cocktail']
dish_in_db = []

for dish in mydishtype:
    db_dishtype = create_dishtype(dish)
    dish_in_db.append(db_dishtype)

    #print(db_dishtype)
    #print(f'<listttttttttt {dish_in_db}>')
#print("\n")
#print(f'<Dish ID ....... {dish_in_db[1].dishtype_id}>')


# cuisine = create_cuisine('american')
mycusine = ['american', 'indian', 'italian', 'mexican', 'chinese', 'vietname', 'korean', 'japanese', 'mediterranean', 'thai' ]
cuisine_in_db = []
for cuisine in mycusine:
    db_cuisine = create_cuisine(cuisine)
    cuisine_in_db.append(db_cuisine)


# diet = create_diet('vegan')
mydiet = ['vegan', 'vegetarian', 'gluteen free', 'diary free', 'mediterranen', 'pescatarian', 'vegan', 'vegan', 'vegan', 'vegan']
diet_in_db=[]
for diet in mydiet:
    db_diet = create_diet(diet)
    diet_in_db.append(db_diet)

print(f'<Diet ID ....... {diet_in_db[0].diet_id}>')
print(diet_in_db[2].diet_id)

#i = creat_ingredient(ingredient = 'potato', unit = 'cup')
mying = ['potato','pancake mix', 'flour', 'chilli powder', 'cheese' ]
myunit= ['each', 'cup', 'cup', 'tbsp', 'oz']
ing_in_db = []
i=0
while i < 5:
    db_ing = create_ingredient(mying[i], myunit[i])
    i +=1
    ing_in_db.append(db_ing)

# for r in range(10):
#         ing = choice(mying)
#         unit = choice(myunit)
#         db_ing = create_ingredient(ing, unit)
#         ing_in_db.append(db_ing)



#recipe = create_recipe('Pancakes', 'this is how you make a pancake. these will be good pancakes.', 0, 0, 1, 1, 1, 'pour batter onto skillet')
rec_title = ['pancake', 'cupcake', 'omlete', 'fried rice', 'sandwitch','cheese burger', 'cake', 'tomato soup', 'falooda', 'mango moose']
rec_des=['pancake', 'cupcake', 'omlete', 'fried rice', 'sandwitch','cheese burger', 'cake', 'tomato soup_desc', 'falooda_desc', 'mango moose_desc']
rec_inst = "instructions"
rec_in_db =[]
i=0
 
while i < 10:

    db_recipe = create_recipe( rec_title[i], f'{rec_des[i]} _desc', i*2, i*4, dish_in_db[i].dishtype_id, cuisine_in_db[i].cuisine_id, diet_in_db[i].diet_id, f'{rec_inst} _ {i}')
    rec_in_db.append(db_recipe)
    i +=1
print("\n")
#print(f'<Reipes in  ....... {db_recipe}>')


# recipeingredient =create_recipeingredient(1, 1, 3)
i = 0
while i < 10:

    for r in range(randint(1, 5)):
        q = randint (1, 5)

        create_recipeingredient(ing_in_db[r].ingredient_id,rec_in_db[i].recipe_id,q)
    i += 1


# rating =  create_rating(4,'very tasty', True, False, 1,1)
i =0
while i < 10:
    rating = randint(1, 5)
    if i % 2 == 0:
        favorite = True
    else:
        favorite = False 

    create_rating(rating,'very tasty', favorite, favorite, rec_in_db[i].recipe_id, user_in_db[i].user_id)
    i+= 1







    


    
