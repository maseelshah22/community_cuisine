from flask import Flask, render_template, request, redirect, url_for, flash
import pymysql.cursors
import hashlib
from forms import LoginForm, RegistrationForm

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
                return True
            return False
    finally:
        connection.close()

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
            return redirect(url_for('index'))
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

@app.route('/')
def index():
    return '''Welcome to Community Cuisine! Please <a href="/login">login</a> or <a href="/register">register</a>.'''


if __name__ == '__main__':
    app.run(debug=True)
