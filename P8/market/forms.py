from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField


class RegisterForm(FlaskForm):
    username = StringField(label='User Name:')
    email_address = StringField(label='Email Address:')
    # two passwords for reconfirmation of the password when registering 
    password1 = PasswordField(label='Password:')
    password2 = PasswordField(label='Confirm Password:') 
    # submit filed
    submit = SubmitField(label='Create Account')

