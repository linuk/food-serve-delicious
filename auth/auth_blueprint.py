from flask import Blueprint, request, redirect, url_for, render_template
from flask_login import logout_user, LoginManager, login_user, login_required, current_user
from passwordhelper import PasswordHelper
from models import db, Users
from forms import UserInfoForm, UserLoginForm

auth_blueprint = Blueprint('auth_blueprint', __name__, template_folder='templates')
login_manager = LoginManager()
ph = PasswordHelper()


@login_manager.user_loader
def load_user(user_id):
    return Users.query.filter_by(id=user_id).first()


@auth_blueprint.record_once
def on_load(state):
    login_manager.init_app(state.app)


@auth_blueprint.route('/')
def index():
    ctas = [
        {'text': 'Sign Up', 'url': url_for('auth_blueprint.register')},
        {'text': 'Sign In', 'url': url_for('auth_blueprint.login')}
    ]
    if current_user.id:
        return redirect(url_for('meals_blueprint.dashboard'))
    return render_template('index.html', ctas=ctas, url_for_index=url_for('meals_blueprint.dashboard'))


@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = UserLoginForm()

    if form.validate_on_submit() and request.method == 'POST':
        email = form.email.data
        password = form.password.data
        user = Users.query.filter_by(email=email).first()
        if ph.validate_password(password, user.salt, user.hashed):
            login_user(user)
            return redirect(url_for('meals_blueprint.dashboard'))

    return render_template('login.html', form=form, url_for_index=url_for('meals_blueprint.dashboard'))


@auth_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = UserInfoForm()

    if form.validate_on_submit() and request.method == 'POST':
        salt = PasswordHelper.get_salt()
        password = form.password.data
        hashed = PasswordHelper.get_hash((salt + password).encode('utf-8'))
        db.session.add(Users(username=form.username.data,
                             email=form.email.data,
                             salt=salt,
                             hashed=hashed))
        db.session.commit()

        user = Users.query.filter_by(email=form.email.data, hashed=hashed).first()
        if user:
            login_user(user)
            return redirect(url_for('meals_blueprint.dashboard'))

    return render_template('register.html', form=form, url_for_index=url_for('meals_blueprint.dashboard'))


@auth_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth_blueprint.index'), url_for_index=url_for('meals_blueprint.dashboard'))
