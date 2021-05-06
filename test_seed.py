from crud import create_user, create_dishtype, create_cuisine, create_diet, create_ingredient, create_recipeingredient, create_recipe, create_rating,get_ingredient_by_name
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


    # dishtype = create_dishtype('snack')
    mydishtype = ['','main course', 'appetizer', 'soup', 'starter', 'fingerfood', 'dessert', 'sauce', 'beverage', 'breakfast', 'bread','side dish']
    dish_in_db = []

    for dish in mydishtype:
        db_dishtype = create_dishtype(dish)
        dish_in_db.append(db_dishtype)


    # cuisine = create_cuisine('american')
    mycusine = ['','American', 'Indian', 'Italian', 'Mexican', 'Chinese', 'Vietnamese', 'Korean', 'Japanese', 'Mediterranean', 'Thai', 'Jewish' ]
    cuisine_in_db = []
    for cuisine in mycusine:
        db_cuisine = create_cuisine(cuisine)
        cuisine_in_db.append(db_cuisine)


    # diet = create_diet('vegan')
    mydiet = ['','Vegan', 'Vegetarian', 'Gluteen Free', 'Whole30', 'Primal', 'Pescetarian', 'Ketogenic', 'Lacto-Vegetarian', 'Ovo-Vegetarian', 'Paleo']
    diet_in_db=[]
    for diet in mydiet:
        db_diet = create_diet(diet)
        diet_in_db.append(db_diet)

    print(f'<Diet ID ....... {diet_in_db[0].diet_id}>')
    print(diet_in_db[2].diet_id)

    #i = creat_ingredient(ingredient = 'potato', unit = 'cup')
    mying = ['other','Eggs','Sugar', 'Butter', 'Milk',  'Bisquick', 'Baking Powder', 'Bread' ]
    myunit= ['each', 'cup', 'tsp', 'tbsp', 'oz']
    ing_in_db = []
    i=0
    while i < 5:
        db_ing = create_ingredient(mying[i], myunit[i])
        i +=1
        ing_in_db.append(db_ing)



    rdata_set = [{
        'title': 'Eggplant Pasta', 'description': 'Easy and quick pasta dish!', 'url': '',
        'instructions': 'Combine all ingredients in bowl. Heat olive oil in a large skillet over medium heat; cook and stir garlic until fragrant, 1 to 2 minutes. Add eggplant; cook, stirring constantly, until eggplant is softened, about 5 minutes. Add tomatoes and juice; cook until sauce is slightly reduced, about 20 minutes. Bring a large pot of lightly salted water to a boil. Cook rigatoni in the boiling water, stirring occasionally until cooked through but firm to the bite, about 13 minutes. Drain and transfer to a serving bowl. Pour sauce over pasta.',
        'prep_time':15,
        'cook_time':40,
        'user_id': 1,
        'dishtype_id': 1,
        'cuisine_id': 1,
        'diet_id': 1,
        'ings' : [['Olive oil', 'cup', 1], ['garlic','Each',5 ], ['Eggplant','each',20], ['Plum Tomatoes','each',5], ['rigatoni pasta','oz',30]]
        }, {
        'title': 'Spicy Roasted Carrots', 'description': 'These tender and roasted carrots cooked in the air fryer can be on your table in less than half an hour. Tossed in a honey-butter sauce and sprinkled with your choice of fresh basil, chives, or just salt and pepper.', 'url': '',
        'instructions': 'Preheat an air fryer to 400 degrees F (200 degrees C). Spray the basket with nonstick cooking spray. Combine butter, honey, orange zest, and cardamom in a bowl. Remove 1 tablespoon of the sauce to a separate bowl and set aside. Add carrots to the remaining sauce and toss until all are well coated. Transfer carrots to the air fryer basket.',
        'prep_time':5,
        'cook_time':20,
        'user_id': 1,
        'dishtype_id': 1,
        'cuisine_id': 1,
        'diet_id': 1,
        'ings' : [['Butter', 'tbsp', 1], ['honey','tbsp', 1 ], ['grated orange','tsp',1], ['cardamom','tsp',1], ['baby carrots','pound',1],['salt', 'pinch', 1]]
        }, {
        'title': 'Stuffed Peppers', 'description': 'Roasted green bell peppers are stuffed with feta cheese and a mixture of rice and green onions', 'url': '',
        'instructions': 'Preheat oven to 400 degrees F (200 degrees C). Lightly grease a baking sheet. In a medium saucepan, bring water to a boil. Stir in the rice. Reduce heat, cover, and simmer for 20 minutes. Remove from heat, and set aside.Place the peppers cut-side down on the prepared baking sheet. Roast 25 to 30 minutes in the preheated oven, or until tender and skin starts to brown.While the peppers are roasting, heat oil in a medium skillet over medium-high heat. Cook the onions, basil, Italian seasoning, salt, and pepper in oil for 2 to 3 minutes. Stir in the tomato, and cook for 5 minutes. Spoon in the cooked rice, and stir until heated through. Remove from heat, mix in the feta cheese, and spoon the mixture into the pepper halves.Return to the oven for 5 minutes. Serve immediately.',
        'prep_time':20,
        'cook_time':40,
        'user_id': 1,
        'dishtype_id': 1,
        'cuisine_id': 1,
        'diet_id': 1,
        'ings' : [['water', 'cup', 1], ['Arborio rice','cup',1 ], ['green bell peppers','each',2], ['olive oil','tbsp',1], ['green onions','each',2], ['basil', 'tsp', 1], ['salt', 'tsp', 1], ['Italian seasoning', 'tsp', 1], ['feta cheese', 'cup', 1]]
        }]

    for rdata in rdata_set:
        db_recipe = create_recipe( rdata['title'], rdata['description'],rdata['prep_time'], rdata['cook_time'],rdata['dishtype_id'], rdata['cuisine_id'],rdata['diet_id'],rdata['instructions'],rdata['url'],rdata['user_id'])
        for ing in rdata['ings']:
            db_ing = get_ingredient_by_name(ing[0])
            if db_ing:
                create_recipeingredient(db_ing.ingredient_id,db_recipe.recipe_id,ing[2])
            else:
                new_ing = create_ingredient(ing[0], ing[1])
                create_recipeingredient(new_ing.ingredient_id,db_recipe.recipe_id,ing[2])

        
        db.session.commit()

if __name__ == "__main__":
    from flask import Flask
    app = Flask(__name__)
    os.system('dropdb testdb')
    os.system('createdb testdb')
    connect_to_db(app, "postgresql:///testdb")
    db.create_all()
    create_example_data()