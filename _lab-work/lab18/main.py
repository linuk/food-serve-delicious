from flask import Flask, redirect, url_for, request, render_template, jsonify
from forms import loginForm, signUpForm, twitForm
from apis import api_route, TwitApi, UsersApi, UsersTwitsApi
from variables import app_secret_key
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from flask_restful import Api
from models import db, Users, Twits
from passwordhelper import PasswordHelper

app = Flask(__name__)
page_title = 'Twits'
app.secret_key = app_secret_key
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://mytwits_user:mytwits_password@localhost/mytwits'
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


@app.route('/', methods=['GET', 'POST'])
def index():
    message = 'You are not logged in.'
    buttons = [
        {'url': url_for('signUp'), 'text': 'Sign Up'},
        {'url': url_for('login'), 'text': 'Login'}
    ]
    form = url_to_edit_twit = url_to_delete_twit = None
    return render_template('index.html', message=message, page_title=page_title, buttons=buttons, twits=[],
                           isLogin=False, form=form, url_to_edit_twit=url_to_edit_twit,
                           url_to_delete_twit=url_to_delete_twit)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = loginForm()
    form_title = 'Login'

    if form.validate_on_submit() and request.method == 'POST':
        username = form.username.data
        password = form.password.data
        user = Users.query.filter_by(username=username).first()
        if ph.validate_password(password, user.salt, user.hashed):
            login_user(user)
            return redirect(url_for('dashboard'))
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
            return redirect(url_for('dashboard'))
    return render_template('form.html', page_title=page_title, form=form, form_title=form_title)


@app.route('/logout')
@login_required
def logout():
    # remove the username from the session if it's there
    logout_user()
    return redirect(url_for('index'))


@app.route('/edit')
@app.route('/edit/<twit_id>', methods=['GET', 'POST'])
@login_required
def edit_twit(twit_id):
    if twit_id is None:
        return redirect(url_for('index'))
    else:
        form = twitForm()
        if form.validate_on_submit():
            twit = Twits.query.filter_by(twit_id=twit_id).first()
            twit.twit = form.twit.data
            db.session.commit()
            return redirect(url_for('dashboard'))

        twit = Twits.query.filter_by(twit_id=twit_id).first()
        return render_template('edit_twit.html', form=form, value=twit.twit)


@app.route('/delete')
@app.route('/delete/<twit_id>', methods=['GET', 'POST'])
@login_required
def delete_twit(twit_id):
    if twit_id is None:
        return redirect(url_for('index'))
    else:
        db.session.delete(Twits.query.filter_by(twit_id=twit_id).first())
        db.session.commit()
        return redirect(url_for('dashboard'))


@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    form = twitForm()
    user_id = current_user.user_id
    print(current_user)
    if form.validate_on_submit():
        twit = Twits(twit=form.twit.data, user_id=user_id)
        db.session.add(twit)
        db.session.commit()

    message = ''
    button_logout = {'url': url_for('logout'), 'text': 'Logout'}
    buttons = [button_logout]
    twits = Users.query.filter_by(user_id=user_id).first().twits
    return render_template('index.html', message=message, page_title=page_title, buttons=buttons, twits=twits,
                           isLogin=True, form=form, url_to_edit_twit=url_for('edit_twit'),
                           url_to_delete_twit=url_for('delete_twit'))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=4000)
