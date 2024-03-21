import pymysql
import random
from flask import Flask
from serpapi import GoogleSearch


def get_db():
    return pymysql.connect(
        host='mysql01.cs.virginia.edu',
        user='dda5us',
        password='d@t@b@s3',
        database='dda5us',
        cursorclass=pymysql.cursors.DictCursor
    )


def create_tables():
    '''
    Creates all necessary tables for the database 
    '''
    with get_db() as connection: 
        with connection.cursor() as cursor:
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    username VARCHAR(255) NOT NULL,
                    email VARCHAR(255) NOT NULL,
                    password VARCHAR(255) NOT NULL,
                    PRIMARY KEY (username),
                    UNIQUE (username, email)
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS person_name (
                    username VARCHAR(255) NOT NULL,
                    first VARCHAR(255) NOT NULL,
                    last VARCHAR(255) NOT NULL,
                    PRIMARY KEY (username),
                    UNIQUE (username)
                )
            ''')

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS food (
                    food_id INT NOT NULL AUTO_INCREMENT,
                    name VARCHAR(255) NOT NULL,
                    ethnic_origin VARCHAR(255) NOT NULL,
                    meal_course VARCHAR(255) NOT NULL,
                    PRIMARY KEY (food_id),
                    UNIQUE (food_id)
                ) 
            ''')

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS recipe (
                    recipe_id INT NOT NULL AUTO_INCREMENT,
                    title VARCHAR(255) NOT NULL,
                    food_id INT NOT NULL,
                    PRIMARY KEY (recipe_id),
                    UNIQUE (recipe_id),
                    FOREIGN KEY (food_id) REFERENCES food(food_id)
                )
            ''')

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS dietary_warnings (
                    recipe_id INT NOT NULL,
                    spice_level INT NOT NULL,
                    restrictions VARCHAR(255) NOT NULL,
                    PRIMARY KEY (recipe_id),
                    UNIQUE (recipe_id),
                    FOREIGN KEY (recipe_id) REFERENCES recipe(recipe_id)
                )
            ''')

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS ingredients (
                    ingredient_id INT NOT NULL AUTO_INCREMENT,
                    name VARCHAR(255) NOT NULL,
                    PRIMARY KEY (ingredient_id),
                    UNIQUE (name)
                )
            ''')

            # I removed quantity, it just complicated things
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS made_of (
                    ingredient_id INT NOT NULL,
                    recipe_id INT NOT NULL,
                    PRIMARY KEY (ingredient_id, recipe_id),
                    UNIQUE (ingredient_id, recipe_id),
                    FOREIGN KEY (ingredient_id) REFERENCES ingredients(ingredient_id),
                    FOREIGN KEY (recipe_id) REFERENCES recipe(recipe_id)
                )
            ''')

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS creates (
                    recipe_id INT NOT NULL,
                    username VARCHAR(255) NOT NULL,
                    PRIMARY KEY (recipe_id, username),
                    UNIQUE (recipe_id, username),
                    FOREIGN KEY (recipe_id) REFERENCES recipe(recipe_id),
                    FOREIGN KEY (username) REFERENCES users(username)
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS reviews (
                    review_id INT NOT NULL AUTO_INCREMENT,
                    recipe_id INT NOT NULL,
                    username VARCHAR(255) NOT NULL,
                    PRIMARY KEY (review_id, recipe_id, username),
                    UNIQUE (review_id, recipe_id, username),
                    FOREIGN KEY (recipe_id) REFERENCES recipe(recipe_id),
                    FOREIGN KEY (username) REFERENCES users(username)
                )
            ''')

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS rating (
                    review_id INT NOT NULL,
                    recipe_id INT NOT NULL,
                    username VARCHAR(255) NOT NULL,
                    star INT NOT NULL,
                    comment VARCHAR(255),
                    PRIMARY KEY (review_id, recipe_id, username),
                    UNIQUE (review_id, recipe_id, username),
                    FOREIGN KEY (review_id) REFERENCES reviews(review_id),
                    FOREIGN KEY (recipe_id) REFERENCES recipe(recipe_id),
                    FOREIGN KEY (username) REFERENCES users(username)
                )
            ''')

            connection.commit()

def populate_database_with_users():
    '''
    Populates the database with users in the user table and person_name table
    '''
    with get_db() as connection:
        with connection.cursor() as cursor:
            cursor.execute('''
                INSERT IGNORE INTO users (username, email, password)
                VALUES ('hayden.johnson', 'cxy6nx@virginia.edu', 'securepassword')
            ''')
            cursor.execute('''
                INSERT IGNORE INTO users (username, email, password)
                VALUES ('maseel.shah', 'dda5us@virginia.edu', 'moresecurepassword')
            ''')
            cursor.execute('''
                INSERT IGNORE INTO users (username, email, password)
                VALUES ('ilyas.jaghoori', 'zyh7ac@virginia.edu', 'evenmoresecurepassword')
            ''')
            cursor.execute('''
                INSERT IGNORE INTO users (username, email, password)
                VALUES ('mohammad.murad', 'vdr4jr@virginia.edu', 'mostsecurepassword')
            ''')
            cursor.execute('''
                INSERT IGNORE INTO person_name (username, first, last)
                VALUES ('hayden.johnson', 'Hayden', 'Johnson')
            ''')
            cursor.execute('''
                INSERT IGNORE INTO person_name (username, first, last)
                VALUES ('maseel.shah', 'Maseel', 'Shah')
            ''')
            cursor.execute('''
                INSERT IGNORE INTO person_name (username, first, last)
                VALUES ('ilyas.jaghoori', 'Ilyas', 'Jaghoori')
            ''')
            cursor.execute('''
                INSERT IGNORE INTO person_name (username, first, last)
                VALUES ('mohammad.murad', 'Mohammad', 'Murad')
            ''')
            connection.commit()

def query_recipe_API():
    '''
    Queries the recipe API and returns a list containing information for one recipe per item
    from the recipe array, using only the name of each food for the query.
    AVOID USING THIS FUNCTION WHEN POSSIBLE, IT WILL USE UP ALL OF YOUR API QUERIES
    '''
    
    recipes = get_recipe_array()

    all_recipes_results = []

    for food in recipes:
        params = {
            "q": food["name"],
            "hl": "en",
            "gl": "us",
            "api_key": "f1364074a82eef5ce493df6854fc7f243f458fd0cc555c46037b584432d39aae"
        }

        search = GoogleSearch(params)
        results = search.get_dict()
        recipe_results = results.get("recipes_results", [])

        if recipe_results:
            recipe_with_name = {**recipe_results[0], "food_name": food["name"]}
            all_recipes_results.append(recipe_with_name)

    return all_recipes_results

def populate_database_with_food_info():
    '''
    Populates the database with food names in the food table
    '''
    with get_db() as connection:
        with connection.cursor() as cursor:
            recipes = get_recipe_array()
            insert_query = '''
                INSERT IGNORE INTO food (name, ethnic_origin, meal_course)
                VALUES (%s, %s, %s)
            '''
            for food in recipes:
                name = food["name"]
                ethnic_origin = food["ethnic_origin"]
                meal_course = food["meal_course"]
                cursor.execute(insert_query, (name, ethnic_origin, meal_course))
            
            connection.commit()

def populate_recipe_table():
    '''
    Populates the recipe table with recipes from the recipe array,
    linking each recipe to its corresponding food item by food_id.
    '''
    recipes = query_recipe_API()

    with get_db() as connection:
        with connection.cursor() as cursor:
            for recipe in recipes:
                title = recipe.get("title")
                food_name = recipe.get("food_name")
                
                cursor.execute('''
                    SELECT food_id FROM food WHERE name = %s
                ''', (food_name,))
                result = cursor.fetchone()

                if result:
                    food_id = result['food_id']
                    
                    cursor.execute('''
                        INSERT IGNORE INTO recipe (title, food_id)
                        VALUES (%s, %s)
                    ''', (title, food_id))
                
            connection.commit()

def populate_ingredients_table():
    '''
    Populates the ingredients table with ingredients from the recipe array,
    converting all ingredient names to lowercase to avoid duplicates based on case sensitivity.
    '''
    recipes = query_recipe_API()

    with get_db() as connection:
        with connection.cursor() as cursor:
            for recipe in recipes:
                ingredients = recipe.get("ingredients", [])
                for ingredient in ingredients:
                    ingredient_lowercase = ingredient.lower()
                    cursor.execute('''
                        INSERT IGNORE INTO ingredients (name)
                        VALUES (%s)
                    ''', (ingredient_lowercase,))

            connection.commit()

def populate_made_of_table():
    '''
    Populates the made_of table with the ingredients and recipes from the recipe array,
    '''
    recipes = query_recipe_API()
    with get_db() as connection:
        with connection.cursor() as cursor:
            for recipe in recipes:
                ingredients = recipe.get("ingredients", [])
                for ingredient in ingredients:
        
                    ingredient_lowercase = ingredient.lower()
                    cursor.execute('''
                        SELECT ingredient_id FROM ingredients WHERE name = %s
                    ''', (ingredient_lowercase,))
                    result = cursor.fetchone()
                    if result:
                        ingredient_id = result['ingredient_id']
                        cursor.execute('''
                            SELECT recipe_id FROM recipe WHERE title = %s
                        ''', (recipe["title"],))
                        result = cursor.fetchone()
                        if result:
                            recipe_id = result['recipe_id']
                            cursor.execute('''
                                INSERT IGNORE INTO made_of (ingredient_id, recipe_id)
                                VALUES (%s, %s)
                            ''', (ingredient_id, recipe_id))
            connection.commit()

def populate_creates_table():
    '''
    Populates the creates table with the recipes and users from the recipe array,
    '''
    usernames = ['hayden.johnson', 'maseel.shah', 'ilyas.jaghoori', 'mohammad.murad']
    
    recipes = query_recipe_API()
    with get_db() as connection:
        with connection.cursor() as cursor:
            for recipe in recipes:
                cursor.execute('''
                    SELECT recipe_id FROM recipe WHERE title = %s
                ''', (recipe["title"],))
                result = cursor.fetchone()
                if result:
                    recipe_id = result['recipe_id']
                    random_username = random.choice(usernames)
                    cursor.execute('''
                        INSERT IGNORE INTO creates (recipe_id, username)
                        VALUES (%s, %s)
                    ''', (recipe_id, random_username))
            connection.commit()

def populate_reviews_table():
    '''
    Populates the reviews table with the recipe_id and username
    '''
    usernames = ['hayden.johnson', 'maseel.shah', 'ilyas.jaghoori', 'mohammad.murad']
    
    recipes = query_recipe_API()
    with get_db() as connection:
        with connection.cursor() as cursor:
            for recipe in recipes:
                cursor.execute('''
                    SELECT recipe_id FROM recipe WHERE title = %s
                ''', (recipe["title"],))
                result = cursor.fetchone()
                if result:
                    recipe_id = result['recipe_id']
                    random_username = random.choice(usernames)
                    cursor.execute('''
                        INSERT IGNORE INTO reviews (recipe_id, username)
                        VALUES (%s, %s)
                    ''', (recipe_id, random_username))
            connection.commit()


def get_recipe_array():
    '''
    Returns an array of dictionaries for our starter foods,
    each dictionary includes the name, ethnic origin, and meal course.
    '''
    recipes = [
        {"name": "Cheesecake", "ethnic_origin": "Western", "meal_course": "Dessert"},
        {"name": "Spaghetti Bolognese", "ethnic_origin": "Italian", "meal_course": "Dinner"},
        {"name": "Chicken Curry", "ethnic_origin": "Indian", "meal_course": "Dinner"},
        {"name": "Vegetable Stir Fry", "ethnic_origin": "Asian", "meal_course": "Dinner"},
        {"name": "Beef Stew", "ethnic_origin": "Western", "meal_course": "Dinner"},
        {"name": "Quiche Lorraine", "ethnic_origin": "French", "meal_course": "Breakfast/Lunch"},
        {"name": "Margherita Pizza", "ethnic_origin": "Italian", "meal_course": "Lunch/Dinner"},
        {"name": "Caesar Salad", "ethnic_origin": "Italian", "meal_course": "Lunch/Dinner"},
        {"name": "Grilled Salmon", "ethnic_origin": "General", "meal_course": "Dinner"},
        {"name": "Ratatouille", "ethnic_origin": "French", "meal_course": "Dinner"},
        {"name": "Pancakes", "ethnic_origin": "Western", "meal_course": "Breakfast"},
        {"name": "Tacos", "ethnic_origin": "Mexican", "meal_course": "Lunch/Dinner"},
        {"name": "Tomato Soup", "ethnic_origin": "General", "meal_course": "Lunch/Dinner"},
        {"name": "Lasagna", "ethnic_origin": "Italian", "meal_course": "Dinner"},
        {"name": "Hamburger", "ethnic_origin": "American", "meal_course": "Lunch/Dinner"},
        {"name": "Pad Thai", "ethnic_origin": "Thai", "meal_course": "Dinner"},
        {"name": "French Onion Soup", "ethnic_origin": "French", "meal_course": "Lunch/Dinner"},
        {"name": "Chocolate Cake", "ethnic_origin": "Western", "meal_course": "Dessert"},
        {"name": "Sushi Rolls", "ethnic_origin": "Japanese", "meal_course": "Lunch/Dinner"},
        {"name": "Banana Bread", "ethnic_origin": "Western", "meal_course": "Breakfast/Dessert"}
    ]
    return recipes                            

def set_up_database():
    create_tables()
    populate_database_with_users()
    populate_database_with_food_info()
    populate_recipe_table()
    populate_ingredients_table()
    populate_made_of_table()
    populate_creates_table()
    populate_reviews_table()




    
        







