from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length

class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8)])

class RegisterForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8)])
