from unittest import TestCase
from server import app
from model import connect_to_db, db
from flask import session, url_for



class FlaskTestRecipes(TestCase):
    def setUp(self):
        """Stuff to do before every test."""

        # # Get the Flask test client
        # self.client = app.test_client()

        # # Show Flask errors that happen during tests
        # app.config['TESTING'] = True
        # connect_to_db(app, "postgresql:///TESTDB")

        # # Create tables and add sample data
        # db.create_all()

        # with self.client as c:
        #     with c.session_transaction() as sess:
        #         sess["user_id"] = 1

    def tearDown(self):
        """Do at end of every test."""

        db.session.remove()
        db.drop_all()
        db.engine.dispose()

    def test_recipe_details(self):
        # Show Flask errors that happen during tests
        app.config['TESTING'] = True
        connect_to_db(app, "postgresql:///TESTDB")

        # Create tables and add sample data
        db.create_all()
        with app.app_context():
            with app.test_request_context():
                with app.test_client() as client:
                    with client.session_transaction() as sess:
                        sess['user_id'] = 1
                        result = client.get("/recipe/details", query_string = {"id": "YR-1"})
                        self.assertEqual(result.status_code, 200)

        

class FlaskTestsBasic(TestCase):
    """Flask tests."""

    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()

        # Show Flask errors that happen during tests
        app.config['TESTING'] = True
        connect_to_db(app, "postgresql:///TESTDB")

        # Create tables and add sample data
        db.create_all()

    def test_index(self):
        """Test homepage page."""

        result = self.client.get("/")
        self.assertEqual(result.status_code, 200)
        self.assertIn(b"Yummy Recipe", result.data)

    def test_login_page(self):
        """ Test login page loaded"""
        result = self.client.get("/login")
        
        self.assertEqual(result.status_code, 200)
        self.assertIn(b"form-signin", result.data)

    def test_signin(self):
        """Test login."""

        result = self.client.post("/signin",
                                  data={"email": "susmi.k@gmail.com", "password": "12345"},
                                  follow_redirects=True)
        self.assertEqual(result.status_code, 200)
        self.assertIn(b"Yummy Recipes", result.data)
    
    # def test_signup(self):
    #     """ Test signup page """
    #     result = self.client.post("/signup",
    #                               data={"email": "sam.k@gmail.com", "password": "12345", "firstname": "sam", "lastname": "k", "mobile-no":"9522234414" },
    #                               follow_redirects=True)
    #     self.assertEqual(result.status_code, 200)
    #     self.assertIn(b"Please Login", result.data)
    

    # def test_logout(self):
    #     """ Test logout page """
    #     result = self.client.post("/logout",
    #                               follow_redirects=True)
    #     self.assertEqual(result.status_code, 200)
    #     
    
class FlaskTestsDatabase(TestCase):
    """Flask tests that use the database."""

    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()
        app.config['TESTING'] = True

        # Connect to test database
        connect_to_db(app, "postgresql:///TESTDB")

        # Create tables and add sample data
        db.create_all()

        self.client.post("/signin",
                                  data={"email": "sam.k@gmail.com", "password": "12345"},
                                  follow_redirects=True)


    # def test_search_route(self):
    #     """Test search result page."""
    #     result = self.client.post("/signin",
    #                               data={"email": "sam.k@gmail.com", "password": "12345"},
    #                               )

    #     #result = self.client.get("/search", data={"search": "pasta"}, follow_redirects=True)
    #     result = self.client.get("/search", query_string={"search": "pancake"}, follow_redirects=True)

    #     #print (result.data)
    #     self.assertEqual(result.status_code, 200)
    #     self.assertIn(b"search", result.data)
        
    # def test_recipe_details(self):
    #     """Test recipe details page."""

    #     # self.client.post("/signin",
    #     #                           data={"email": "sam.k@gmail.com", "password": "12345"},
    #     #                           follow_redirects=True)

    #     with self.client.session_transaction() as sess:

    #         sess['user_id'] = 1
    #         sess['fname'] = "sam"
    #         result = self.client.get("/recipe/details", query_string={"id ": "YR-1"}, follow_redirects=True)
    #         print ("++++++++++++ /details+++++++++++",self.client)
        
    #     #import pdb; pdb.set_trace()

    #     print(result.data)
    #     self.assertEqual(result.status_code, 200)
    #     self.assertIn(b"Italian Wedding Soup", result.data)

#         

#     def tearDown(self):
#         """Do at end of every test."""

#         db.session.remove()
#         db.drop_all()
#         db.engine.dispose()




# class FlaskTestsLoggedIn(TestCase):
#     """Flask tests with user logged in to session."""

#     def setUp(self):
#         """Stuff to do before every test."""

#         app.config['TESTING'] = True
#         app.config['RAPIDAPI_KEY'] = 'key'
#         self.client = app.test_client()

#         with self.client as c:
#             with c.session_transaction() as sess:
#                 sess['user_id'] = 1

#     def test_important_page(self):
#         """Test important page."""

#         result = self.client.get("/important")
#         self.assertIn(b"You are a valued user", result.data)


# class FlaskTestsLoggedOut(TestCase):
#     """Flask tests with user logged in to session."""

#     def setUp(self):
#         """Stuff to do before every test."""

#         app.config['TESTING'] = True
#         self.client = app.test_client()

#     def test_important_page(self):
#         """Test that user can't see important page when logged out."""

#         result = self.client.get("/important", follow_redirects=True)
#         self.assertNotIn(b"You are a valued user", result.data)
#         self.assertIn(b"You must be logged in", result.data)


# class FlaskTestsLogInLogOut(TestCase):  # Bonus example. Not in lecture.
#     """Test log in and log out."""

#     def setUp(self):
#         """Before every test"""

#         app.config['TESTING'] = True
#         self.client = app.test_client()

#     def test_login(self):
#         """Test log in form.

#         Unlike login test above, 'with' is necessary here in order to refer to session.
#         """

#         with self.client as c:
#             result = c.post('/login',
#                             data={'user_id': '42', 'password': 'abc'},
#                             follow_redirects=True
#                             )
#             self.assertEqual(session['user_id'], '42')
#             self.assertIn(b"You are a valued user", result.data)

#     def test_logout(self):
#         """Test logout route."""

#         with self.client as c:
#             with c.session_transaction() as sess:
#                 sess['user_id'] = '42'

#             result = self.client.get('/logout', follow_redirects=True)

#             self.assertNotIn(b'user_id', session)
#             self.assertIn(b'Logged Out', result.data)


if __name__ == "__main__":
    import unittest

    unittest.main()
