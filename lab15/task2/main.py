from flask import Flask, session, redirect, url_for, escape, request, render_template, abort
from forms import loginForm, signUpForm, twitForm
from dbhelper import DBHelper
from variables import app_secret_key

app = Flask(__name__)
page_title = 'Task 1'
app.secret_key = app_secret_key
dbhelper = DBHelper()


@app.route('/', methods=['GET', 'POST'])
def index():
    if 'isLogin' in session:
        form = twitForm()
        user_id = session['user_id']
        if form.validate_on_submit():
            twit = form['twit'].data
            dbhelper.add_a_new_twit(user_id, twit)

        isLogin = True
        message = 'Logged in as %s' % escape(session['username'])
        button_logout = {'url': url_for('logout'), 'text': 'Logout'}
        buttons = [button_logout]
        twits = dbhelper.get_all_twits(user_id)
        if len(twits) > 0:
            twits.reverse()
        url_to_edit_twit = url_for('edit_twit')
        url_to_delete_twit = url_for('delete_twit')
    else:
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
        result = dbhelper.get_user_id_by_username_and_password(username, password)
        if result is not None:
            session['username'] = request.form['username']
            session['user_id'] = result['user_id']
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

@app.route('/edit')
@app.route('/edit/<twit_id>', methods=['GET', 'POST'])
def edit_twit(twit_id):
    if not session.get('username'):
        abort(401)
    if twit_id == None:
        return redirect(url_for('index'))
    else:
        form = twitForm()
        if form.validate_on_submit():
            twit = request.form['twit']
            dbhelper.update_a_twit(twit_id, twit)
            return redirect(url_for('index'))

        twit = dbhelper.get_a_twit(twit_id)
        return render_template('edit_twit.html', form=form, value=twit['twit'])


@app.route('/delete')
@app.route('/delete/<twit_id>', methods=['GET', 'POST'])
def delete_twit(twit_id):
    if not session.get('username'):
        abort(401)
    if twit_id != None:
        dbhelper.delete_twit(twit_id)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=4000)
