from flask import Flask, render_template, request, flash, redirect, url_for

app = Flask(__name__)
app.secret_key = 'some_secret'
USERNAME = 'admin'
PASSWORD = '1234'


@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if not validateLogin(request.form['username'], request.form['password']):
            error = 'Invalid credentials'
        else:
            flash('Login Succeed.')
            return redirect(url_for('done'))
    return render_template('login_before.html', error=error)


@app.route('/login', methods=['GET', 'POST'])
def done():
    return render_template('login_after.html')


def validateLogin(username, password):
    return username == USERNAME and password == PASSWORD


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=4000)
