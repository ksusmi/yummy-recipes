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

