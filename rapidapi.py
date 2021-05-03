import requests
import os
#from server import app
from flask import Flask
app = Flask(__name__)

#app.secret_key = 'SECRETSECRETSECRET'

# This configuration option makes the Flask interactive debugger
# more useful (you should remove this line in production though)
app.config['PRESERVE_CONTEXT_ON_EXCEPTION'] = True

try:
    API_KEY = os.environ['RAPIDAPI_KEY']    
except KeyError: 
    print("*****RAPID-API: Environment variable does not exist")
    print(f"*****RAPID-API: Environment variables {os.environ}")


url = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/"

headers = {
        'x-rapidapi-key': API_KEY,
        'x-rapidapi-host': "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com"
        }

def get_recipe_details_by_id(recipeid):

    recipe_info_endpoint = "recipes/{0}/information".format(recipeid)
    ingedientsWidget = "recipes/{0}/ingredientWidget".format(recipeid)
    equipmentWidget = "recipes/{0}/equipmentWidget".format(recipeid)

    recipe_info = requests.request("GET", url + recipe_info_endpoint, headers=headers).json()
        
    headers["accept"] = "text/html"
    querystring = {"defaultCss":"true", "showBacklink":"false"}

    recipe_info['inregdientsWidget'] = requests.request("GET", url + ingedientsWidget, headers=headers, params=querystring).text
    recipe_info['equipmentWidget'] = requests.request("GET", url + equipmentWidget, headers=headers, params=querystring).text
    
    # Remove additional headers
    del headers["accept"]

    return recipe_info

def get_recipe_by_ingredients(ingredients):

    recipe_info_endpoint = "recipes/findByIngredients"
    querystring = {"ingredients":ingredients,"number":"5","ranking":"1","ignorePantry":"true"}
    recipe_info = requests.request("GET", url + recipe_info_endpoint, headers=headers, params=querystring).json()

    return recipe_info

def get_recipe_nutriinfo(recipeid):

    recipe_info_endpoint = "recipes/{0}/nutritionWidget.json".format(recipeid)
    response = requests.request("GET", url + recipe_info_endpoint, headers=headers)
    return response.json()

#def get_recipe_info_widget(recipeid):

def get_recipe_complex_search(**filters):
    querystring = {}
    recipe_info_endpoint = "recipes/complexSearch" #"recipes/search"
    #cuisine=cuisine, exclude_cuisine=exclude_cuisine, diet=diet, intolerances=intolerances, equipment=equipment, include_ingredients=include_ingredients, exclude_ingredients=exclude_ingredients
    #querystring = {"query":query,"diet":"vegetarian","excludeIngredients":"coconut","intolerances":"egg, gluten","number":"10","offset":"0","type":"main course"}
    querystring = filters
    recipe_info = requests.request("GET", url + recipe_info_endpoint, headers=headers, params=querystring).json()

    return recipe_info

def get_equipment_list_by_recipe_id(recipeid):
    recipe_info_endpoint = "/recipes/{0}/equipmentWidget.json".format(recipeid)
    response = requests.request("GET", url+recipe_info_endpoint, headers=headers)
    return response.json()

def get_random_food_joke():
    recipe_info_endpoint = "/food/jokes/random"
    response = requests.request("GET", url + recipe_info_endpoint, headers=headers)
    return response.json()

def get_random_food_trivia():
    recipe_info_endpoint = "/food/trivia/random"
    response = requests.request("GET", url + recipe_info_endpoint, headers=headers)
    return response.json()

def get_ingredients_list_of_recipe(recipeid):
    
    recipe_info_endpoint = "/recipes/{0}/ingredientWidget.json".format(recipeid)
    response = requests.request("GET", url+ recipe_info_endpoint, headers=headers)
    return response.json()

def get_random_recipe():
    recipe_info_endpoint = "/recipes/random"
    querystring = {"number":"1","tags":"vegetarian,dessert"}
    response = requests.request("GET", url+recipe_info_endpoint, headers=headers, params=querystring)
    return response.json()

def  get_visualize_recipe_ingredient(recipeid):
    recipe_info_endpoint = "/recipes/1003464/ingredientWidget"
    response = requests.request("GET", url+recipe_info_endpoint, headers=headers)
    return response.json()

def get_visualize_recipe_nutrition_widget(recipeid):
    recipe_info_endpoint = "/recipes/{0}/nutritionWidget".format(recipeid)
    headers["accept"]: "text/html" 
    response = requests.request("GET", url+recipe_info_endpoint, headers=headers)
    del headers["accept"]
    return response.json()


