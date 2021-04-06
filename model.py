"""Models for Search recipes app."""

from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


# Replace this with your code!
class User(db.Model):
    """A user."""

    __tablename__ = 'users'

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True,)
    fname = db.Column(db.String, nullable = False,)
    lname = db.Column(db.String, nullable = False,)
    email = db.Column(db.String, unique=True, nullable = False,)
    # password should have to be or no ?
    password = db.Column(db.String, nullable = False, )
    mobile_no = db.Column(db.Integer, nullable = True,)

    def __repr__(self):
        #print (f'<User user_id={self.user_id} email={self.email}>')
        return f'<User user_id={self.user_id} email={self.email}>'


class DishType(db.Model):
    """A dist type."""

    __tablename__ = 'dishtypes'

    dishtype_id = db.Column(db.Integer, autoincrement=True, primary_key=True,)
    dishtype_name = db.Column(db.String, nullable = False,)
    
    def __repr__(self):
        #print (f'<User user_id={self.user_id} email={self.email}>')
      #  return f'<User user_id={self.user_id} email={self.email}>'

class Cuisine(db.Model):
    """A cuisine."""

    __tablename__ = 'cuisines'

    cuisine_id = db.Column(db.Integer, autoincrement=True, primary_key=True,)
    cuisine_name = db.Column(db.String, nullable = False,)
   

    def __repr__(self):
        #print (f'<User user_id={self.user_id} email={self.email}>')
        #return f'<User user_id={self.user_id} email={self.email}>'

class Diet(db.Model):
    """A diet."""

    __tablename__ = 'diets'

    diet_id = db.Column(db.Integer, autoincrement=True, primary_key=True,)
    diet_name = db.Column(db.String, nullable = False,)
   

    def __repr__(self):
        #print (f'<User user_id={self.user_id} email={self.email}>')
      #  return f'<User user_id={self.user_id} email={self.email}>'

class Ingredient(db.Model):
    """A ingredients."""

    __tablename__ = 'ingredients'

    ingredient_id = db.Column(db.Integer, autoincrement=True, primary_key=True,)
    ingredient = db.Column(db.String, nullable = False,)
    unit = db.Column(db.String, nullable = False,)
    

    def __repr__(self):
        #print (f'<User user_id={self.user_id} email={self.email}>')
       # return f'<User user_id={self.user_id} email={self.email}>'

class RecipeIngredient(db.Model):
    """A recipe ingredients."""

    __tablename__ = 'recipeingredients'

    ingredient_id =db.Column(db.Integer, db.ForeignKey('ingredients.ingredient_id'))
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.recipe_id'))
    quantity = db.Column(db.String, nullable = False,)
    
    ingredient = db.relationship('Ingredient', backref='recipeingredients')
    recipe = db.relationship('Recipe', backref='recipeingredients')

    def __repr__(self):
        #print (f'<User user_id={self.user_id} email={self.email}>')
       # return f'<User user_id={self.user_id} email={self.email}>'


class Recipe(db.Model):
    """A Recipe ."""

    __tablename__ = 'recipes'

    recipe_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.Text)
    #####????????????????????????
    prep_time =
    cook_time =
    dish_type_id =db.Column(db.Integer, db.ForeignKey('dishtypes.dish_type_id'))
    cuisine_id = db.Column(db.Integer, db.ForeignKey('cuisines.cuisine_id'))
    diet_id = db.Column(db.Integer, db.ForeignKey('diets.diet_id'))
    rinstructions

    # release_date = db.Column(db.DateTime)
    # poster_path = db.Column(db.String)

    # ratings = a list of Rating objects

    dishtype = db.relationship('DishType', backref='recipes')
    cuisine = db.relationship('Cuisine', backref='recipes')
    diet = db.relationship('Diet', backref='recipes')

    def __repr__(self):
       # return f'<Movie movie_id={self.movie_id} title={self.title}>'

class UserFavoriteAndReview(db.Model):
    """A User favorite, review and rating."""

    __tablename__ = 'userfavoriteandreviews'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.recipe_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    ####????????????
    rating = db.Column(db.Integer)
    review_notes = db.Column(db.Text)
    #?????????????
    favorite =
    
    # ???????????
    external

    recipe = db.relationship('Recipe', backref='userfavoriteandreviews')
    user = db.relationship('User', backref='userfavoriteandreviews')

    def __repr__(self):
       # return f'<Rating rating_id={self.rating_id} score={self.score}>'


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
