"""Models for Search recipes app."""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


db = SQLAlchemy()

class User(db.Model):
    """A user."""

    __tablename__ = 'users'

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True,)
    fname = db.Column(db.String, nullable = False,)
    lname = db.Column(db.String, nullable = False,)
    email = db.Column(db.String, unique=True, nullable = False,)
    password = db.Column(db.String, nullable = False, )
    mobile_no = db.Column(db.String, nullable = True,)

    def __repr__(self):
        return f'<User user_id={self.user_id} email={self.email} fname= {self.fname}>'


class DishType(db.Model):
    """A dish type."""

    __tablename__ = 'dishtypes'

    dishtype_id = db.Column(db.Integer, autoincrement=True, primary_key=True,)
    dishtype_name = db.Column(db.String, nullable = False,)
    
    def __repr__(self):
        return f'<DishType dishtype_id={self.dishtype_id} dishtype_name={self.dishtype_name}>'


class Cuisine(db.Model):
    """A cuisine."""

    __tablename__ = 'cuisines'

    cuisine_id = db.Column(db.Integer, autoincrement=True, primary_key=True,)
    cuisine_name = db.Column(db.String, nullable = False,)
   

    def __repr__(self):
        return f'<Cuisine cuisine_id={self.cuisine_id} cuisine_name={self.cuisine_name}>'


class Diet(db.Model):
    """A diet."""

    __tablename__ = 'diets'

    diet_id = db.Column(db.Integer, autoincrement=True, primary_key=True,)
    diet_name = db.Column(db.String, nullable = False,)
   

    def __repr__(self):  
        return f'<Diet diet_id={self.diet_id} diet_name={self.diet_name}>'


class Ingredient(db.Model):
    """A ingredients."""

    __tablename__ = 'ingredients'

    ingredient_id = db.Column(db.Integer, autoincrement=True, primary_key=True,)
    ingredient = db.Column(db.String, nullable = False,)
    unit = db.Column(db.String, nullable = False,)
    

    def __repr__(self):
        return f'<Ingredient ingredient_id={self.ingredient_id} ingredient={self.ingredient} unit = {self.unit}>'


class RecipeIngredient(db.Model):
    """A recipe ingredients."""

    __tablename__ = 'recipeingredients'

    recipeingredient_id = db.Column(db.Integer, autoincrement=True, primary_key=True,)
    ingredient_id =db.Column(db.Integer, db.ForeignKey('ingredients.ingredient_id'))
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.recipe_id'))
    quantity = db.Column(db.String, nullable = False,)
    ingredient = db.relationship('Ingredient', backref='recipeingredients')
    recipe = db.relationship('Recipe', backref='recipeingredients')

    def __repr__(self):
        return f'<RecipeIngredient ingredient_id={self.ingredient_id} recipe_id={self.recipe_id} quantity={self.quantity}>'



class Recipe(db.Model):
    """A Recipe ."""

    __tablename__ = 'recipes'

    recipe_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.Text)
    prep_time = db.Column(db.Integer, nullable = True,)
    cook_time = db.Column(db.Integer, nullable = True,)
    dishtype_id =db.Column(db.Integer, db.ForeignKey('dishtypes.dishtype_id'))
    user_id =db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable = False)
    cuisine_id = db.Column(db.Integer, db.ForeignKey('cuisines.cuisine_id'))
    diet_id = db.Column(db.Integer, db.ForeignKey('diets.diet_id')) 
    instructions = db.Column(db.Text)
    url = db.Column(db.String, nullable = True)

    dishtype = db.relationship('DishType', backref='recipes')
    cuisine = db.relationship('Cuisine', backref='recipes')
    diet = db.relationship('Diet', backref='recipes')
    user = db.relationship('User', backref='recipes')

    def __repr__(self):
        return f'<Recipe recipe_id={self.recipe_id} title={self.title}>'



class Rating(db.Model):
    """A User favorite, review and Rating."""

    __tablename__ = 'ratings'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    recipe_id =  db.Column(db.Integer, nullable = False)
    title_ext = db.Column(db.String)
    description_ext = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable = False)
    rating = db.Column(db.Integer)
    review_notes = db.Column(db.Text)   
    favorite = db.Column(db.Boolean, default= False,)
    external = db.Column(db.Boolean, default = False,)
    
    user = db.relationship('User', backref='ratings')


    def __repr__(self):
        return f'<Rating id={self.id} recipe_id={self.recipe_id} user_id={self.user_id} rating={self.rating} review_notes={self.review_notes} favorite={self.favorite} external={self.external}>'


def connect_to_db(flask_app, db_uri='postgresql:///searchrecipe', echo=False):
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    flask_app.config['SQLALCHEMY_ECHO'] = echo
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.app = flask_app
    db.init_app(flask_app)

    print('Connected to the db!')

    


if __name__ == '__main__':
    # since my server.py is not ready so for now commenting and using below
    #from server import app
    from flask import Flask
    app = Flask(__name__)

    # Call connect_to_db(app, echo=False) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.

    connect_to_db(app)
