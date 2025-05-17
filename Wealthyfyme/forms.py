from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length,Regexp

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    remember = BooleanField('I agree to the Terms & Conditions', validators=[DataRequired()])
    submit = SubmitField('Log In')

class RegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=50),Regexp(r'^[A-Za-z ]+$', message="Name must contain only letters and spaces")])
    email = StringField('Email', validators=[DataRequired(), Email(message="Invalid email format"),Regexp(r'^\S+@\S+\.\S+$', message="Invalid email format")])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6),Regexp(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{6,}$',message="Password must include uppercase, lowercase, digit, and special character")])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message="Passwords must match")])
    accept_terms = BooleanField('I agree to the Terms & Conditions', validators=[DataRequired()])
    submit = SubmitField('Register')    
