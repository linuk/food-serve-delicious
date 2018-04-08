from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateTimeField, DateField, validators, FileField, SubmitField, \
    IntegerField, FloatField


class UserInfoForm(FlaskForm):
    """For user registering and editing"""
    username = StringField('username', validators=[validators.DataRequired()])
    email = StringField('email', validators=[validators.DataRequired(), validators.Email()])
    password = PasswordField('password', validators=[validators.DataRequired()])
    re_password = PasswordField('re_password', validators=[validators.DataRequired(), validators.EqualTo('password')])
    submit = SubmitField('submit', validators=[validators.DataRequired()])


class UserLoginForm(FlaskForm):
    email = StringField('email', validators=[validators.DataRequired(), validators.Email()])
    password = PasswordField('password', validators=[validators.DataRequired()])
    submit = SubmitField('submit', validators=[validators.DataRequired()])


class MealInfoForm(FlaskForm):
    name = StringField('name', validators=[validators.DataRequired()])
    description = StringField('description', validators=[validators.DataRequired()])
    image = FileField('image')
    guest_num = IntegerField('guest_num', validators=[validators.DataRequired(), validators.number_range(0)])
    time = DateField('time', validators=[validators.DataRequired()])
    price = FloatField('price', validators=[validators.DataRequired()])
    lat = FloatField('lat', validators=[validators.DataRequired()])
    lng = FloatField('lng', validators=[validators.DataRequired()])
    user_id = IntegerField('user_id', validators=[validators.DataRequired(), validators.number_range(0)])
    submit = SubmitField('submit', validators=[validators.DataRequired()])


class DashboardSearchForm(FlaskForm):
    postcode = StringField('postcode', validators=[validators.DataRequired()])
    submit = SubmitField('submit', validators=[validators.DataRequired()])
