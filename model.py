"""Models for Search recipes app."""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


db = SQLAlchemy()


# Replace this with your code!
class User(db.Model):
    """A user."""

    __tablename__ = 'users'

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True,)
    fname = db.Column(db.String, nullable = False,)
    lname = db.Column(db.String, nullable = False,)
    email = db.Column(db.String, unique=True, nullable = False,)
    # password should have to be mixed characters? and display as *
    password = db.Column(db.String, nullable = False, )
    mobile_no = db.Column(db.Integer, nullable = True,)

    def __repr__(self):
        return f'<User user_id={self.user_id} email={self.email}>'


class DishType(db.Model):
    """A dist type."""

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
    #####????????????????????????
    prep_time = db.Column(db.Integer, nullable = True,)
    cook_time = db.Column(db.Integer, nullable = True,)
    dish_type_id =db.Column(db.Integer, db.ForeignKey('dishtypes.dish_type_id'))
    cuisine_id = db.Column(db.Integer, db.ForeignKey('cuisines.cuisine_id'))
    diet_id = db.Column(db.Integer, db.ForeignKey('diets.diet_id'))
    instructions = db.Column(db.Text,)

    dishtype = db.relationship('DishType', backref='recipes')
    cuisine = db.relationship('Cuisine', backref='recipes')
    diet = db.relationship('Diet', backref='recipes')

    def __repr__(self):
        return f'<Recipe recipe_id={self.recipe_id} title={self.title} description={self.description} prep_time={self.prep_time} cook_time={self.cook_time} dish_type_id={self.dish_type_id} cuisine_id={self.cuisine_id} diet_id={self.diet_id} instructions={self.instructions} >'



class UserFavoriteAndReview(db.Model):
    """A User favorite, review and rating."""

    __tablename__ = 'userfavoriteandreviews'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.recipe_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    rating = db.Column(db.Integer)
    review_notes = db.Column(db.Text)
    #????????????? yes or no / true or false
    favorite = db.Column(db.
    
    # ??????????? boolean
    external = db.Column(db.Boolean, default = False,)
    
    #########?????? error
    recipe =db.relationship('Recipe', backref='userfavoriteandreviews')
    user = db.relationship('User', backref='userfavoriteandreviews')

    def __repr__(self):
        return f'<UserFavoriteAndReview id={self.id} recipe_id={self.recipe_id} user_id={self.user_id} rating={self.rating} review_notes={self.review_notes} favorite={self.favorite} external={self.external}>'


def connect_to_db(flask_app, db_uri='postgresql:///ratings', echo=True):
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    flask_app.config['SQLALCHEMY_ECHO'] = echo
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.app = flask_app
    db.init_app(flask_app)

    print('Connected to the db!')

    


if __name__ == '__main__':
    from server import app

    # Call connect_to_db(app, echo=False) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.

    connect_to_db(app)
