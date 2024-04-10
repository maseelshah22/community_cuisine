from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField, IntegerField, HiddenField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional, NumberRange

WTF_CSRF_CHECK_DEFAUL = False

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=25)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    first_name = StringField('First Name', validators=[DataRequired(), Length(max=50)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(max=50)])
    submit = SubmitField('Register')

class RecipeForm(FlaskForm):
    title = StringField('Recipe Title', validators=[DataRequired(), Length(min=3, max=255)])
    ingredients = TextAreaField('Ingredients', validators=[DataRequired()])
    submit = SubmitField('Submit Recipe')

class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Update')

class RecipeForm(FlaskForm):
    name = StringField('Food Name', validators=[DataRequired()])
    ethnic_origin = StringField('Ethnic Origin', validators=[DataRequired()])
    meal_course = SelectField('Meal Course', choices=[('Breakfast', 'Breakfast'), ('Lunch', 'Lunch'), ('Dinner', 'Dinner'), ('Dessert', 'Dessert')], validators=[DataRequired()])
    title = StringField('Recipe Title', validators=[DataRequired()])
    spice_level = IntegerField('Spice Level (1-5)', validators=[DataRequired()])
    restrictions = StringField('Dietary Restrictions', validators=[Optional()])
    ingredients = StringField('Ingredients (comma-separated)', validators=[DataRequired()])
    submit = SubmitField('Add Recipe')

class RatingForm(FlaskForm):
    recipe_id = HiddenField('Recipe ID')
    star = IntegerField('Rating (1-5)', validators=[DataRequired(), NumberRange(min=1, max=5)])
    comment = TextAreaField('Comment', validators=[DataRequired()])
    submit = SubmitField('Submit Review')



