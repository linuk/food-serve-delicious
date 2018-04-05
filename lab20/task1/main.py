from flask import Flask, redirect, url_for, request, render_template, jsonify
from forms import loginForm, signUpForm
from apis import api_route, TwitApi, UsersApi, UsersTwitsApi
from variables import app_secret_key
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from flask_restful import Api
from models import db, Users
from passwordhelper import PasswordHelper
from twits_blueprint import twits_blueprint

page_title = 'Twits'
app = Flask(__name__)
app.secret_key = app_secret_key
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://mytwits_user:mytwits_password@localhost/mytwits'
app.register_blueprint(twits_blueprint)

ph = PasswordHelper()
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)

api = Api(app)
api.add_resource(TwitApi, api_route('twits/<int:twit_id>'), api_route('twits'))
api.add_resource(UsersApi, api_route('users/<int:user_id>'))
api.add_resource(UsersTwitsApi, api_route('users/<int:user_id>/twits'))


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


@app.route('/login_blueprint', methods=['GET', 'POST'])
def login():
    form = loginForm()
    form_title = 'Login'

    if form.validate_on_submit() and request.method == 'POST':
        username = form.username.data
        password = form.password.data
        user = Users.query.filter_by(username=username).first()
        if ph.validate_password(password, user.salt, user.hashed):
            login_user(user)
            return redirect(url_for('twits_blueprint.dashboard'))
    return render_template('form.html', page_title=page_title, form=form, form_title=form_title)


@app.route('/signUp', methods=['GET', 'POST'])
def signUp():
    form_title = 'Sign Up'
    form = signUpForm()

    if form.validate_on_submit() and request.method == 'POST':

        salt = ph.get_salt().decode('utf-8')
        password = form.password.data
        username = form.username.data
        hashed = ph.get_hash((salt + password).encode('utf-8'))
        user = Users(username=username, password=password, salt=salt, hashed=hashed)
        db.session.add(user)
        db.session.commit()

        user = Users.query.filter_by(username=form.username.data, hashed=hashed).first()
        if user:
            login_user(user)
            return redirect(url_for('twits_blueprint.dashboard'))
    return render_template('form.html', page_title=page_title, form=form, form_title=form_title)


@app.route('/logout')
@login_required
def logout():
    # remove the username from the session if it's there
    logout_user()
    return redirect(url_for('twits_blueprint.index'))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=4000)
