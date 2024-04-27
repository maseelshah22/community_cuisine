from flask import Flask, render_template, request, redirect, url_for, flash, session
import pymysql.cursors
import hashlib
from forms import LoginForm, RegistrationForm, RecipeForm, UpdateAccountForm, RatingForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'bomboclaat_lebron_james_you_are_my_sunshine'

def get_db():
    return pymysql.connect(
        host='mysql01.cs.virginia.edu',
        user='dda5us',
        password='d@t@b@s3',
        database='dda5us',
        cursorclass=pymysql.cursors.DictCursor
    )

def register_user(username, email, password, first_name, last_name):
    connection = get_db()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
            if cursor.fetchone() is not None:
                return "Username already exists"
            
            cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
            if cursor.fetchone() is not None:
                return "Email already exists"

            cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)", 
                           (username, email, hash_password(password)))
            cursor.execute("INSERT INTO person_name (username, first, last) VALUES (%s, %s, %s)", 
                           (username, first_name.capitalize(), last_name.capitalize()))
            connection.commit()
    finally:
        connection.close()
    return "User registered successfully"


def login_user(username, password):
    connection = get_db()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
            user = cursor.fetchone()
            if user and user['password'] == hash_password(password):
                session['username'] = username
                return True
            return False
    finally:
        connection.close()

@app.route('/find')
def find_page():
    if 'username' in session:
        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT first, last FROM person_name WHERE username = %s', (session['username'],))
        user = cursor.fetchone()
        if user:
            first_name, last_name = user['first'], user['last']
            return render_template('find.html', title='FindPage', first_name=first_name, last_name=last_name)
    return render_template('find.html', title='FindPage')

@app.route('/search', methods=['POST'])
def search():
    search_term = request.form['search_term']
    db = get_db()
    cursor = db.cursor()

    if 'username' in session:
        cursor.execute('SELECT first, last FROM person_name WHERE username = %s', (session['username'],))
        user = cursor.fetchone()
        if user:
            first_name, last_name = user['first'], user['last']
        else:
            first_name, last_name = None, None
    else:
        first_name, last_name = None, None

    cursor.execute('SELECT * FROM food WHERE name LIKE %s', ('%' + search_term + '%',))
    food_items = cursor.fetchall()

    recipes = []
    for food in food_items:
        cursor.execute('SELECT * FROM recipe WHERE food_id = %s', (food['food_id'],))
        recipe_info = cursor.fetchall()
        recipes.extend(recipe_info)

    return render_template('find.html', recipes=recipes, first_name=first_name, last_name=last_name)


@app.route('/recipe/<int:recipe_id>')
def show_ingredients(recipe_id):
    db = get_db() 
    cursor = db.cursor() 

    cursor.execute('SELECT recipe_id, title, average_rating, URL FROM recipe WHERE recipe_id = %s', (recipe_id,))
    recipe = cursor.fetchone() 
    

    cursor.execute('''
        SELECT name FROM ingredients 
        JOIN made_of ON ingredients.ingredient_id = made_of.ingredient_id
        WHERE made_of.recipe_id = %s
    ''', (recipe_id,))

    ingredients = cursor.fetchall()

    cursor.execute('''
        SELECT username, star, comment FROM rating 
        WHERE recipe_id = %s
    ''', (recipe_id,))
    ratings = cursor.fetchall()

    cursor.execute('''
        SELECT spice_level, restrictions FROM dietary_warnings 
        WHERE recipe_id = %s
    ''', (recipe_id,))
    restrictions = cursor.fetchall()

    cursor.execute('''
        SELECT users.username FROM creates
        JOIN users ON creates.username = users.username
        WHERE creates.recipe_id = %s
    ''', (recipe_id,))

    creator_person = cursor.fetchone()
    creator = creator_person['username']


    db = get_db()
    cursor = db.cursor()

    if 'username' in session:
        cursor.execute('SELECT first, last FROM person_name WHERE username = %s', (session['username'],))
        user = cursor.fetchone()
        if user:
            first_name, last_name = user['first'], user['last']
        else:
            first_name, last_name = None, None
    else:
        first_name, last_name = None, None
    
    return render_template('ingredients.html', recipe=recipe, ingredients=ingredients, ratings=ratings, restrictions=restrictions, first_name=first_name, last_name=last_name, creator=creator)

@app.route('/update_account', methods=['GET', 'POST'])
def update_account():
    if 'username' not in session:
        return redirect(url_for('login'))
        
    form = UpdateAccountForm()
    if request.method == 'POST' and form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = hash_password(form.password.data)

        try:
            connection = get_db()
            with connection.cursor() as cursor:
                sql = "UPDATE users SET email = %s, password = %s WHERE username = %s"
                cursor.execute(sql, (email, password, username))
            connection.commit()
        finally:
            connection.close()

        flash('Your account has been updated!', 'success')
        return redirect(url_for('find_page')) 
    elif request.method == 'GET':
        try:
            connection = get_db()
            with connection.cursor() as cursor:
                sql = "SELECT username, email FROM users WHERE username = %s"
                cursor.execute(sql, (session['username'],))
                result = cursor.fetchone()
                form.username.data = result['username']
                form.email.data = result['email']
        finally:
            connection.close()

    db = get_db()
    cursor = db.cursor()

    if 'username' in session:
        cursor.execute('SELECT first, last FROM person_name WHERE username = %s', (session['username'],))
        user = cursor.fetchone()
        if user:
            first_name, last_name = user['first'], user['last']
        else:
            first_name, last_name = None, None
    else:
        first_name, last_name = None, None

    return render_template('update_account.html', title='Update Account', form=form, first_name=first_name, last_name=last_name)

def hash_password(password):
    salt = "5wf5t9GUcqlSQxMe"
    salted_password = password + salt
    hash_object = hashlib.sha256(salted_password.encode())
    hashed_password = hash_object.hexdigest()
    return hashed_password


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if login_user(form.username.data, form.password.data):
            flash('Logged in successfully!')
            return redirect(url_for('find_page')) #THING I CHANGED FOR LOG IN REDIRECT
        else:
            flash('Invalid username or password.')
    return render_template('login.html', title='Login', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        result = register_user(form.username.data, form.email.data, form.password.data, form.first_name.data, form.last_name.data)
        if result == "User registered successfully":
            flash('Account created successfully! Please log in.')
            return redirect(url_for('login'))
        else:
            flash(result) 
    return render_template('register.html', title='Register', form=form)

@app.route('/add_recipe', methods=['GET', 'POST'])
def add_recipe():
    form = RecipeForm()
    if form.validate_on_submit():
        name = form.name.data
        ethnic_origin = form.ethnic_origin.data
        meal_course = form.meal_course.data
        title = form.title.data
        spice_level = form.spice_level.data
        restrictions = form.restrictions.data
        ingredients_list = [i.strip() for i in form.ingredients.data.split(',')]
        URL = form.URL.data

        connection = get_db()
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT food_id FROM food WHERE LOWER(name) LIKE LOWER(%s)", ('%' + name + '%',))
                food = cursor.fetchone()
                if food is None:
                    cursor.execute("INSERT INTO food (name, ethnic_origin, meal_course) VALUES (%s, %s, %s)", (name, ethnic_origin, meal_course))
                    food_id = connection.insert_id()
                else:
                    food_id = food['food_id']
    
                    
                cursor.execute("INSERT INTO recipe (title, food_id, URL) VALUES (%s, %s, %s)", (title, food_id, URL))
                recipe_id = cursor.lastrowid

                cursor.execute("INSERT INTO dietary_warnings (recipe_id, spice_level, restrictions) VALUES (%s, %s, %s)", (recipe_id, spice_level, restrictions))

                for ingredient_name in ingredients_list:
                    cursor.execute("SELECT ingredient_id FROM ingredients WHERE LOWER(name) LIKE LOWER(%s)", ('%' + ingredient_name + '%',))
                    ingredient = cursor.fetchone()
                    if ingredient is None:
                        cursor.execute("INSERT INTO ingredients (name) VALUES (%s)", (ingredient_name.lower(),))
                        ingredient_id = cursor.lastrowid
                    else:
                        ingredient_id = ingredient['ingredient_id']

                    cursor.execute("INSERT INTO made_of (ingredient_id, recipe_id) VALUES (%s, %s)", (ingredient_id, recipe_id))

                
                username = session['username'] 
                cursor.execute("INSERT INTO creates (recipe_id, username) VALUES (%s, %s)", (recipe_id, username))

                connection.commit()
                
                flash('Recipe added successfully!', 'success')
        except Exception as e:
            flash(f'An error occurred: {e}', 'danger')
        finally:
            connection.close()

        return redirect(url_for('find_page'))
    
    db = get_db()
    cursor = db.cursor()

    if 'username' in session:
        cursor.execute('SELECT first, last FROM person_name WHERE username = %s', (session['username'],))
        user = cursor.fetchone()
        if user:
            first_name, last_name = user['first'], user['last']
        else:
            first_name, last_name = None, None
    else:
        first_name, last_name = None, None

    return render_template('add_recipe.html', title='Add New Recipe', form=form, first_name=first_name, last_name=last_name)


@app.route('/add_rating/<int:recipe_id>', methods=['GET', 'POST'])
def add_rating(recipe_id):
    print(recipe_id)
    form = RatingForm()
    if form.validate_on_submit():
        star = form.star.data
        comment = form.comment.data
        username = session['username']
        
        connection = get_db()
        try:
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO reviews (recipe_id, username) VALUES (%s, %s)", (recipe_id, username))
                review_id = cursor.lastrowid
                
                cursor.execute("INSERT INTO rating (review_id, recipe_id, username, star, comment) VALUES (%s, %s, %s, %s, %s)", (review_id, recipe_id, username, star, comment))
                connection.commit()
                flash('Rating added successfully!', 'success')
        finally:
            connection.close()
        return redirect(url_for('show_ingredients', recipe_id=recipe_id))
    
    db = get_db()
    cursor = db.cursor()

    if 'username' in session:
        cursor.execute('SELECT first, last FROM person_name WHERE username = %s', (session['username'],))
        user = cursor.fetchone()
        if user:
            first_name, last_name = user['first'], user['last']
        else:
            first_name, last_name = None, None
    else:
        first_name, last_name = None, None
    return render_template('add_rating.html', title='Add Rating', form=form, recipe_id=recipe_id,first_name=first_name, last_name=last_name)

@app.route('/user_reviews')
def user_reviews():
    
    if 'username' not in session:
        flash('Please log in to view your reviews.', 'warning')
        return redirect(url_for('login'))
    
    

    username = session['username']
    db = get_db()
    cursor = db.cursor()

    if 'username' in session:
        cursor.execute('SELECT first, last FROM person_name WHERE username = %s', (session['username'],))
        user = cursor.fetchone()
        if user:
            first_name, last_name = user['first'], user['last']
        else:
            first_name, last_name = None, None
    else:
        first_name, last_name = None, None

    cursor.execute('''
        SELECT DISTINCT rating.review_id, recipe.title, rating.star, rating.comment 
        FROM reviews
        INNER JOIN rating ON reviews.recipe_id = rating.recipe_id AND reviews.username = rating.username
        INNER JOIN recipe ON rating.recipe_id = recipe.recipe_id
        WHERE reviews.username = %s
    ''', (username,))
    reviews = cursor.fetchall()

    return render_template('user_reviews.html', reviews=reviews,first_name=first_name, last_name=last_name)

@app.route('/delete_review/<int:review_id>')
def delete_review(review_id):
    if 'username' not in session:
        flash('Please log in to continue.', 'warning')
        return redirect(url_for('login'))

    username = session['username']
    db = get_db()
    cursor = db.cursor()

    cursor.execute('SELECT * FROM rating WHERE review_id = %s AND username = %s', (review_id, username))
    review = cursor.fetchone()

    if review:
        cursor.execute('DELETE FROM rating WHERE review_id = %s', (review_id,))
        db.commit()
        flash('Review deleted successfully.', 'success')
    else:
        flash('Unauthorized deletion attempt.', 'danger')

    return redirect(url_for('user_reviews'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


@app.route('/')
def index():
    db = get_db()
    cursor = db.cursor()

    if 'username' in session:
        cursor.execute('SELECT first, last FROM person_name WHERE username = %s', (session['username'],))
        user = cursor.fetchone()
        if user:
            first_name, last_name = user['first'], user['last']
        else:
            first_name, last_name = None, None
    else:
        first_name, last_name = None, None
    return render_template('index.html', title='Index',first_name=first_name, last_name=last_name)


if __name__ == '__main__':
    app.run(debug=True)
