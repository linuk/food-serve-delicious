from flask import Flask, session, redirect, url_for, escape, request, render_template, abort
from forms import loginForm, signUpForm, twitForm
from dbhelper import DBHelper
from variables import app_secret_key
from flask_login import LoginManager, login_required, login_user, logout_user
from user import User

app = Flask(__name__)
page_title = 'Task 1'
app.secret_key = app_secret_key
db = DBHelper()

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    result = db.get_user(user_id)
    if result:
        return User(user_id)


@app.route('/', methods=['GET', 'POST'])
def index():
    isLogin = False
    message = 'You are not logged in.'
    button_signUp = {'url': url_for('signUp'), 'text': 'Sign Up'}
    button_signIn = {'url': url_for('login'), 'text': 'Login'}
    buttons = [button_signUp, button_signIn]
    twits = []
    form = url_to_edit_twit = url_to_delete_twit = None
    return render_template('index.html', message=message, page_title=page_title, buttons=buttons, twits=twits,
                           isLogin=isLogin, form=form, url_to_edit_twit=url_to_edit_twit, url_to_delete_twit=url_to_delete_twit)


@app.route('/login', methods=['GET', 'POST'])
def login():

    form = loginForm()
    form_title = 'Login'

    if form.validate_on_submit() and request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_id = db.check_password(username, password)
        if user_id:
            user = User(user_id)
            login_user(user)
            return redirect(url_for('dashboard'))
    return render_template('form.html', page_title=page_title, form=form, form_title=form_title)


@app.route('/signUp', methods=['GET', 'POST'])
def signUp():

    form_title = 'Sign Up'
    form = signUpForm()

    if form.validate_on_submit() and request.method == 'POST':

        # Insert user data
        username = request.form['username']
        password = request.form['password']
        db.add_user(username, password)

        # Pull user data
        user_id = db.check_password(username, password)
        if user_id:
            user = User(user_id)
            login_user(user)
            return redirect(url_for('dashboard'))
    return render_template('form.html', page_title=page_title, form=form, form_title=form_title)


@app.route('/logout')
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
            twit = request.form['twit']
            db.update_a_twit(twit_id, twit)
            return redirect(url_for('dashboard'))

        twit = db.get_a_twit(twit_id)
        return render_template('edit_twit.html', form=form, value=twit['twit'])
    

@app.route('/delete')
@app.route('/delete/<twit_id>', methods=['GET', 'POST'])
@login_required
def delete_twit(twit_id):
    if twit_id is None:
        return redirect(url_for('index'))
    else:
        db.delete_twit(twit_id)
        return redirect(url_for('dashboard'))


@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    form = twitForm()
    user_id = session['user_id']
    if form.validate_on_submit():
        twit = form['twit'].data
        db.add_a_new_twit(user_id, twit)

    isLogin = True
    message = ''
    button_logout = {'url': url_for('logout'), 'text': 'Logout'}
    buttons = [button_logout]
    twits = db.get_all_twits(user_id)
    if len(twits) > 0:
        twits.reverse()
    url_to_edit_twit = url_for('edit_twit')
    url_to_delete_twit = url_for('delete_twit')
    return render_template('index.html', message=message, page_title=page_title, buttons=buttons, twits=twits,
                           isLogin=isLogin, form=form, url_to_edit_twit=url_to_edit_twit, url_to_delete_twit=url_to_delete_twit)



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=4000)
