import pymysql
from flask import Flask

def get_db():
    return pymysql.connect(
        host='mysql01.cs.virginia.edu',
        user='dda5us',
        password='d@t@b@s3',
        database='dda5us',
        cursorclass=pymysql.cursors.DictCursor
    )

# creating necessary tables
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
                UNIQUE (ingredient_id)
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS made_of (
                ingredient_id INT NOT NULL,
                recipe_id INT NOT NULL,
                quantity INT NOT NULL,
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
        







