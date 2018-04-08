# /usr/bin/python3

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators, PasswordField


class twitForm(FlaskForm):
    twit = StringField('twit', validators=[validators.DataRequired()])
    submit = SubmitField('submit', validators=[validators.DataRequired()])


class loginForm(FlaskForm):
    username = StringField('username', validators=[validators.DataRequired()])
    password = PasswordField('password', validators=[validators.DataRequired()])
    submit = SubmitField('submit', validators=[validators.DataRequired()])


class signUpForm(FlaskForm):
    username = StringField('username', validators=[validators.DataRequired()])
    password = PasswordField('password', validators=[validators.DataRequired()])
    submit = SubmitField('submit', validators=[validators.DataRequired()])
