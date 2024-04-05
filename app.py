from flask import Flask, render_template, request, redirect, url_for, flash, session
import pymysql.cursors
import hashlib
from forms import LoginForm, RegistrationForm, RecipeForm

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

@app.route('/home')
def home_page():
    if 'username' in session:
        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT first, last FROM person_name WHERE username = %s', (session['username'],))
        user = cursor.fetchone()
        if user:
            first_name, last_name = user['first'], user['last']
            return render_template('home.html', title='HomePage', first_name=first_name, last_name=last_name)
    return render_template('home.html', title='HomePage')

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

    return render_template('home.html', recipes=recipes, first_name=first_name, last_name=last_name)


@app.route('/recipe/<int:recipe_id>')
def show_ingredients(recipe_id):
    db = get_db() 
    cursor = db.cursor() 

    cursor.execute('SELECT title, average_rating FROM recipe WHERE recipe_id = %s', (recipe_id,))
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
    
    return render_template('ingredients.html', recipe=recipe, ingredients=ingredients, ratings=ratings)


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
            return redirect(url_for('home_page')) #THING I CHANGED FOR LOG IN REDIRECT
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

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.')
    return redirect(url_for('index'))


@app.route('/')
def index():
    return render_template('index.html', title='Index')


if __name__ == '__main__':
    app.run(debug=True)
