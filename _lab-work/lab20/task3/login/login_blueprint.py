from flask import Blueprint, render_template, request, url_for, redirect
from flask_login import login_user, logout_user, login_required, LoginManager
from passwordhelper import PasswordHelper
from forms import loginForm, signUpForm
from models import db, Users

login_blueprint = Blueprint('login_blueprint', __name__, template_folder='templates')
login_manager = LoginManager()
ph = PasswordHelper()


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


@login_blueprint.record_once
def on_load(state):
    login_manager.init_app(state.app)


@login_blueprint.route('/login', methods=['GET', 'POST'])
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
    return render_template('form.html', page_title='Login', form=form, form_title=form_title)


@login_blueprint.route('/signUp', methods=['GET', 'POST'])
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
    return render_template('form.html', page_title='Sign Up', form=form, form_title=form_title)


@login_blueprint.route('/logout')
@login_required
def logout():
    # remove the username from the session if it's there
    logout_user()
    return redirect(url_for('twits_blueprint.index'))
