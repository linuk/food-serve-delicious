from flask import Flask, session, redirect, url_for, escape, request, render_template
from forms import loginForm, signUpForm
from dbhelper import DBHelper
from variables import app_secret_key

app = Flask(__name__)
page_title = 'Task 1'
app.secret_key = app_secret_key
dbhelper = DBHelper()


@app.route('/')
def index():
    if 'isLogin' in session:
        isLogin = True
        message = 'Logged in as %s' % escape(session['username'])
        button_logout = {'url': url_for('logout'), 'text': 'Logout'}
        buttons = [button_logout]
        user_id = session['user_id']
        twits = dbhelper.get_all_twits(user_id)
    else:
        isLogin = False
        message = 'You are not logged in.'
        button_signUp = {'url': url_for('signUp'), 'text': 'Sign Up'}
        button_signIn = {'url': url_for('login'), 'text': 'Login'}
        buttons = [button_signUp, button_signIn]
        twits = []
    return render_template('index.html', message=message, page_title=page_title, buttons=buttons, twits=twits,
                           isLogin=isLogin)


@app.route('/login', methods=['GET', 'POST'])
def login():

    form = loginForm()
    form_title = 'Login'

    if form.validate_on_submit() and request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        result = dbhelper.get_user_id_by_username_and_password(username, password)
        if result is not None:
            session['username'] = request.form['username']
            session['user_id'] = result[0]
            session['isLogin'] = True
            return redirect(url_for('index'))
    return render_template('form.html', page_title=page_title, form=form, form_title=form_title)


@app.route('/signUp', methods=['GET', 'POST'])
def signUp():

    form_title = 'Sign Up'
    form = signUpForm()

    if form.validate_on_submit() and request.method == 'POST':

        # Insert user data
        username = request.form['username']
        password = request.form['password']
        dbhelper.add_user(username, password)

        # Pull user data
        result = dbhelper.get_user_id_by_username_and_password(username, password)
        if result is not None:
            session['username'] = username
            session['user_id'] = dbhelper.get_user_id_by_username_and_password(username, password)[0]
            session['isLogin'] = True
            return redirect(url_for('index'))
    return render_template('form.html', page_title=page_title, form=form, form_title=form_title)


@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('isLogin', None)
    session.pop('username', None)
    session.pop('user_id', None)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=4000)
