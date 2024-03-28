from flask import Flask, render_template, request, redirect, url_for, flash
import pymysql.cursors
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

def register_user(username, email, password):
    connection = get_db()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE username = %s OR email = %s", (username, email))
            if cursor.fetchone() is not None:
                return False
            
            cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)", (username, email, password))
            connection.commit()
    finally:
        connection.close()
    return True

def login_user(username, password):
    connection = get_db()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
            user = cursor.fetchone()
            if user and user['password'] == password:
                return True
            return False
    finally:
        connection.close()

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
        if register_user(form.username.data, form.email.data, form.password.data):
            flash('Account created successfully! Please log in.')
            return redirect(url_for('login'))
        else:
            flash('Username or email already exists.')
    return render_template('register.html', title='Register', form=form)

@app.route('/')
def index():
    return '''Welcome to Community Cuisine! Please <a href="/login">login</a> or <a href="/register">register</a>.'''


if __name__ == '__main__':
    app.run(debug=True)