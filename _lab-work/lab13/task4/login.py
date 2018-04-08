from flask import Flask, render_template, flash, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, length

app = Flask(__name__)
app.secret_key = 'some_secret'
USERNAME = 'admin'
PASSWORD = 'asd'


class LoginForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired(), length(min=3)])
    submit = SubmitField('submit', validators=[DataRequired()])


@app.route('/', methods=['GET', 'POST'])
def form():
    error = None
    form = LoginForm()
    app.logger.debug("Form")
    if form.validate_on_submit():
        app.logger.debug("Validated")
        username = form.username.data
        password = form.password.data
        if validateLogin(username, password):
            return redirect('login')
        else:
            error = "The username or password is wrong."

    return render_template('form.html', error=error, form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')


def validateLogin(username, password):
    return username == USERNAME and password == PASSWORD


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=4000)
