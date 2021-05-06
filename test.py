from unittest import TestCase
from server import app
from model import connect_to_db, db
from flask import session

import test_seed
import server

def mock_get_recipe_details_by_id(recipe_id):
    return {"title": "TITLE", 
            "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/11/Test-Logo.svg/783px-Test-Logo.svg.png",
            "id": "ID",
            "instructions": "INSTRUCTIONS",
            "summary": "SUMMARY",
            "cuisines": "CUSINES",
            "dishTypes": "DISHTYPES",
            "diets": "DIETS",
            "vegan": "VEGAN",
            "vegetarian": "VEGETARIAN",
            "glutenFree": "GLUTENFREE",
            "dairyFree": "DAIRYFREE",
            "veryHealthy": "VERYHEALTHY",
            "pricePerServing": "PRICEPERSERVING",
            "readyInMinutes": "READYINMINUTES",
            "inregdientsWidget": "INGREDIENTSWIDGET",
            "equipmentWidget": "EQUIPMENTWIDGET"
            }

def mock_get_recipe_nutriinfo(recipe_id):
    return {"calories": "CALORIES", "carbs": "CARBS", "fat": "FAT", "protein": "PROTEIN", "bad_nutri": "BAD_NUTRI", "good_nutri": "GOOD_NUTRI" }

# def mock_get_dishtype():
#     return {"1": "snack"}

# def mock_get_diet():
#     return {"1": "vegan"}

# def mock_get_cuisine():
#     return {"1": "Indian"}

# def mock_get_ingredients():
#     return {"1": "flour", "2": "salt", "3":"pepper"}

# def mock_get_unit():
#     return {"1": "cup", "2": "tbsp", "3":"tbsp"}

class FlaskTestBasic(TestCase):
    """ Flask tests. """

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'key'
        connect_to_db(app, "postgresql:///testdb")
        db.create_all()
        test_seed.create_example_data()

    def test_index(self):
       """Test homepage page."""

       result = self.client.get("/")
       self.assertEqual(result.status_code, 200)
       self.assertIn(b"Yummy Recipe", result.data)

    def test_signup(self):
        """ Test signup page """
        result = self.client.post("/signup",
                                  data={"email": "susmi.k@gmail.com", "password": "12345", "firstname": "sam", "lastname": "k", "mobile-no":"9522234414" },
                                  follow_redirects=True)
        self.assertEqual(result.status_code, 200)
        self.assertIn(b"Yummy Recipe", result.data)

    
    def test_login_page(self):
        """ Test login page loaded"""
        result = self.client.get("/login")
        self.assertEqual(result.status_code, 200)
      

    def test_signin(self):
        """Test login."""

        result = self.client.post("/signin",
                                  data={"email": "user0@gmail.com", "password": "test0"},
                                  follow_redirects=True)
        self.assertEqual(result.status_code, 200)
        self.assertIn(b"Yummy Recipes", result.data)
 

    def test_logout(self):
        """ Test logout page """
        result = self.client.get("/logout",
                                  follow_redirects=True)
        self.assertIn(b"Logged Out", result.data)
        self.assertEqual(result.status_code, 200)

    def test_duplicate_signup(self):
        """ Test signup page """
        result = self.client.post("/signup",
                              data={"email": "sr.k@gmail.com", "password": "12345", "firstname": "sam", "lastname": "k", "mobile-no":"9522234414" },
                              follow_redirects=True)
        self.assertEqual(result.status_code, 200)
        self.assertIn(b"Please Login", result.data)
         
    def tearDown(self):
        """Do at end of every test."""
        db.session.remove()
        db.drop_all()
        db.engine.dispose()

class FlaskTestRecipes(TestCase):
    def setUp(self):
        """Stuff to do before every test."""

        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'key'
        self.client = app.test_client()

        server.rapidapi.get_recipe_details_by_id = mock_get_recipe_details_by_id
        server.rapidapi.get_recipe_nutriinfo = mock_get_recipe_nutriinfo

        # Connect to test database
        connect_to_db(app, "postgresql:///testdb")
        # Create tables and add sample data
        db.create_all()
        test_seed.create_example_data()

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = 1
                sess['fname'] = "jill0"
    
    def tearDown(self):
        """Do at end of every test."""
        db.session.remove()
        db.drop_all()
        db.engine.dispose()

    def test_search_route(self):
        """Test search result page."""
        result = self.client.post("/signin",
                                  data={"email": "sam.k@gmail.com", "password": "12345"},
                                  )
        #result = self.client.get("/search", data={"search": "pasta"}, follow_redirects=True)
        result = self.client.get("/search", query_string={"search": "pancake"}, follow_redirects=True)
        self.assertEqual(result.status_code, 200)
        self.assertIn(b"search", result.data)

    def test_recipe_details(self):
        result = self.client.get("/recipe/details", query_string = {"id": "YR-1"})
        print("*"*20)
        print(result.data)
        self.assertEqual(result.status_code, 200)

    def test_create_your_recipe(self):
        result = self.client.get('/add-your-recipe', query_string = {'recipe-title':"Title", "description": "Description", "instructions": "Instructions", "ingredients": "Ingredients", "measure":"Measure", "quantity":"Quantity"})
        print("*"*40)
        print(result.data)
        self.assertEqual(result.status_code, 200)

    def test_fav_link(self):
        result = self.client.get('/add-your-recipe', query_string = {'recipe-title':"Title", "instructions": "Instructions", "ingredients": "Ingredients", "measure":"Measure", "quantity":"Quantity"})
        print("*"*40)
        print(result.data)
        self.assertEqual(result.status_code, 200)

  
if __name__ == "__main__":
    import unittest

    unittest.main()