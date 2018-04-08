from flask import Flask, session, redirect, url_for, escape, request, render_template

app = Flask(__name__)
app_secret_key = 'asdlihasldigqwelkjasldih laishdl'
page_title = 'Task 1'
app.secret_key = app_secret_key


@app.route('/')
def index():
    if 'username' in session:
        message = 'Logged in as %s' % escape(session['username'])
        CTA_url = url_for('logout')
        CTA_text = 'logout'
    else:
        message = 'You are not logged in.'
        CTA_url = url_for('login')
        CTA_text = 'login'
    return render_template('index.html', message=message, page_title=page_title, CTA_url=CTA_url, CTA_text=CTA_text)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('index'))
    return render_template('login_form.html', page_title=page_title)


@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=4000)
