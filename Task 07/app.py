import requests
from flask import   Flask, render_template, request

app = Flask(__name__)

 
MEALDB_SEARCH = "https://www.themealdb.com/api/json/v1/1/search.php?s="
MEALDB_ID = "https://www.themealdb.com/api/json/v1/1/lookup.php?i="
MEALDB_LETTER = "https://www.themealdb.com/api/json/v1/1/search.php?f="
MEALDB_CATEGORIES = "https://www.themealdb.com/api/json/v1/1/list.php?c=list"
MEALDB_CATEGORY = "https://www.themealdb.com/api/json/v1/1/filter.php?c="




@app.route('/')
def home():
    try:
        featured = []
        for letter in ['a', 'b', 'c']:
            resp = requests.get(MEALDB_LETTER + letter)
            data = resp.json()
            if data['meals']:
                featured.extend(data['meals'][:2])
        return render_template('index.html', featured=featured)
    except:
        return render_template('index.html', featured=[])

@app.route('/search')
def search():
    """Search for recipes by name"""
    food = request.args.get('food')
    if not food:
        return render_template('search.html', meals=None)
    
    try:
        resp = requests.get(MEALDB_SEARCH + food)
        data = resp.json()
        
        if data['meals'] is None:
            return render_template('search.html', meals=None, error=f"No recipes for '{food}'")
        
        return render_template('search.html', meals=data['meals'], food=food)
    except Exception as e:
        return render_template('search.html', meals=None, error=str(e))

def extract_ingredients(meal_data):
    """Extract ingredients and measures from meal data"""
    ingredients = []
    for i in range(1, 21):  
        ing_key = f'strIngredient{i}'
        measure_key = f'strMeasure{i}'
        
        if ing_key in meal_data and meal_data[ing_key]:
            ingredient = meal_data[ing_key].strip()
            measure = meal_data[measure_key].strip() if measure_key in meal_data else ""
            
            if ingredient:
                ingredients.append({
                    'ingredient': ingredient,
                    'measure': measure
                })
    return ingredients
def estimate_prep_and_cooking_times(category):
    """Estimate cooking time based on recipe category"""
    times = {
        'Seafood': {'prep': '10-15 mins', 'cooking': '15-20 mins'},
        'Chicken': {'prep': '10-15 mins', 'cooking': '20-30 mins'},
        'Beef': {'prep': '15-20 mins', 'cooking': '30-45 mins'},
        'Pasta': {'prep': '10-15 mins', 'cooking': '15-20 mins'},
        'Dessert': {'prep': '15-25 mins', 'cooking': '20-30 mins'},
        'Breakfast': {'prep': '5-10 mins', 'cooking': '10-15 mins'},
        'Vegetarian': {'prep': '10-15 mins', 'cooking': '15-25 mins'},
        'Vegan': {'prep': '10-15 mins', 'cooking': '15-25 mins'},
    }
    return times.get(category, {'prep': '15-20 mins', 'cooking': '20-30 mins'})

@app.route('/meal/<meal_id>')
def meal(meal_id):
    """Get specific meal by ID"""
    try:
        resp = requests.get(MEALDB_ID + meal_id)
        data = resp.json()
        
        if data['meals'] is None:
            return render_template('meal.html', meal=None, error="Meal not found")
        
        meal_data = data['meals'][0]
        ingredients = extract_ingredients(meal_data)
        times = estimate_prep_and_cooking_times(meal_data.get('strCategory', ''))
        
        return render_template('meal.html', meal=meal_data, ingredients=ingredients, prep_time=times['prep'], cooking_time=times['cooking'])
    except Exception as e:
        return render_template('meal.html', meal=None, error=str(e))

@app.route('/letter/<letter>')
def browse(letter):
    """Browse recipes by letter"""
    letter = letter.lower()
    
    try:
        resp = requests.get(MEALDB_LETTER + letter)
        data = resp.json()
        
        if data['meals'] is None:
            meals = []
        else:
            meals = data['meals']
        
        return render_template('browse.html', meals=meals, letter=letter.upper())
    except Exception as e:
        return render_template('browse.html', meals=[], letter=letter.upper(), error=str(e))

@app.route('/categories')
def categories_list():
    """Show all recipe categories"""
    try:
        resp = requests.get(MEALDB_CATEGORIES)
        data = resp.json()
        categories = data['meals'] if data['meals'] else []
        return render_template('categories.html', categories=categories)
    except Exception as e:
        return render_template('categories.html', categories=[], error=str(e))
@app.route('/category/<name>')
def category(name):
    """Get recipes in a category"""
    try:
        resp = requests.get(MEALDB_CATEGORY + name)
        data = resp.json()
        
        if data['meals'] is None:
            meals = []
        else:
            meals = data['meals']
        
        return render_template('category_meals.html', meals=meals, category=name)
    except Exception as e:
        return render_template('category_meals.html', meals=[], category=name, error=str(e))

@app.route('/shopping-list')
def shopping_list():
    """Show shopping list from localStorage"""
    return render_template('shopping_list.html')

if __name__ == "__main__":
    app.run(host='localhost', port=8080, debug=True)
