from flask import Flask, render_template, redirect, url_for, request
from pymongo import MongoClient
from pymysql import connect as sql_connect
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import input_required

app = Flask(__name__)
app.secret_key = 'klahyfagloug2to871h9y0*^(*Hiyf1o3hg7936f1'
app.config['database'] = 'mytwits'
app.config['table'] = 'twits'
app.config['mysql_username'] = 'mytwits_user'
app.config['mysql_password'] = 'mytwits_password'
app.config['mysql_host'] = 'localhost'
app.config['default_user_id'] = 1
app.config['default_username'] = 'dan1'


class AddTwitForm(FlaskForm):
    username = StringField('username', validators=[input_required()])
    twit = StringField('twit', validators=[input_required()])
    submit = SubmitField('submit', validators=[input_required()])


class EditTwitForm(FlaskForm):
    twit = StringField('twit', validators=[input_required()])
    submit = SubmitField('submit', validators=[input_required()])


class DBHelper_mongo:

    def __init__(self):
        client = MongoClient()
        self.db = client[app.config['database']]

    def get_all_twits(self):
        return self.db[app.config['table']].find().sort('created_at', -1)

    def add_a_new_twit(self, twit):
        new_twit = {
            'twit': twit,
            'username': app.config['default_username'],
            'created_at': datetime.utcnow(),
        }
        return self.db[app.config['table']].insert(new_twit)


class DBHelper_mysql:

    def __init__(self):
        self.db = sql_connect(
            host=app.config['mysql_host'],
            database=app.config['database'],
            user=app.config['mysql_username'],
            passwd=app.config['mysql_password'],
        )

    def get_all_twits(self):
        with self.db.cursor() as cursor:
            query = 'SELECT u.username, t.twit, t.created_at FROM twits t, users u WHERE t.user_id=u.user_id ORDER BY t.created_at DESC '
            cursor.execute(query)
            return cursor.fetchall()

    def add_a_new_twit(self, twit):
        user_id = app.config['default_user_id']
        with self.db.cursor() as cursor:
            query = 'INSERT INTO twits (twit, user_id) VALUES("{}", "{}")'.format(twit, user_id)
            cursor.execute(query)
            return self.db.commit()


app.config['dbHelper_mongo'] = DBHelper_mongo()
app.config['dbHelper_mysql'] = DBHelper_mysql()


@app.route('/')
def index():
    return redirect(url_for('show_twits_mongo'))


@app.route('/mongo', methods=['GET', 'POST'])
def show_twits_mongo():
    form = AddTwitForm()
    if form.validate_on_submit():
        twit = form['twit'].data
        res = app.config['dbHelper_mongo'].add_a_new_twit(twit)

    twits = app.config['dbHelper_mongo'].get_all_twits()
    mysql_url = url_for('show_twits_mysql')
    mongo_url = url_for('show_twits_mongo')

    return render_template('show_twits.html', twits=twits, type='mongo', mysql_url=mysql_url, mongo_url=mongo_url,
                           default_username=app.config['default_username'], form=form)


@app.route('/mysql', methods=['GET', 'POST'])
def show_twits_mysql():
    form = AddTwitForm()

    # If a new twit is submitted
    if form.validate_on_submit():
        twit = form['twit'].data
        res = app.config['dbHelper_mysql'].add_a_new_twit(twit)

    twits = app.config['dbHelper_mysql'].get_all_twits()
    mysql_url = url_for('show_twits_mysql')
    mongo_url = url_for('show_twits_mongo')

    return render_template('show_twits.html', twits=twits, type='mysql', mysql_url=mysql_url, mongo_url=mongo_url,
                           default_username=app.config['default_username'], form=form)


if __name__ == '__main__':
    app.run(debug=True, port=4000, host='0.0.0.0')
