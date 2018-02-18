from flask import Flask, render_template, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
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


class TwitForm(FlaskForm):
    username = StringField('username')
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

    def get_a_twit(self, twit_id):
        return self.db[app.config['table']].find_one({'_id': ObjectId(twit_id)})

    def update_a_twit(self, twit, twit_id):
        return self.db[app.config['table']].update_one({'_id': ObjectId(twit_id)}, {'$set': {'twit': twit, 'created_at': datetime.utcnow()}})

    def delete_a_twit(self, twit_id):
        return self.db[app.config['table']].delete_one({'_id': ObjectId(twit_id)})


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
            query = 'SELECT u.username, t.twit, t.created_at, t.twit_id FROM twits t, users u WHERE t.user_id=u.user_id ORDER BY t.created_at DESC '
            cursor.execute(query)
            return cursor.fetchall()

    def get_a_twit(self, twit_id):
        with self.db.cursor() as cursor:
            query = 'SELECT u.username, t.twit, t.created_at, t.twit_id from twits t, users u WHERE twit_id={} and u.user_id=t.user_id'.format(
                twit_id)
            cursor.execute(query)
            return cursor.fetchone()

    def add_a_new_twit(self, twit):
        user_id = app.config['default_user_id']
        with self.db.cursor() as cursor:
            query = 'INSERT INTO twits (twit, user_id) VALUES("{}", "{}")'.format(twit, user_id)
            cursor.execute(query)
            return self.db.commit()

    def update_a_twit(self, twit_id, twit):
        with self.db.cursor() as cursor:
            query = 'UPDATE twits SET twit="{}", created_at="{}" WHERE twit_id={}'.format(twit, datetime.utcnow(),
                                                                                          twit_id)
            print(query)
            cursor.execute(query)
            return self.db.commit()

    def delete_twit(self, twit_id):
        with self.db.cursor() as cursor:
            query = 'DELETE FROM twits WHERE twit_id = {}'.format(twit_id)
            cursor.execute(query)
            return self.db.commit()


app.config['dbHelper_mongo'] = DBHelper_mongo()
app.config['dbHelper_mysql'] = DBHelper_mysql()


@app.route('/')
def index():
    return redirect(url_for('show_twits_mongo'))


@app.route('/mongo', methods=['GET', 'POST'])
def show_twits_mongo():
    db = app.config['dbHelper_mongo']
    form = TwitForm()

    if form.validate_on_submit():
        twit = form['twit'].data
        db.add_a_new_twit(twit)

    twits = db.get_all_twits()
    mysql_url = url_for('show_twits_mysql')
    mongo_url = url_for('show_twits_mongo')

    return render_template('show_twits.html', twits=twits, type='mongo', mysql_url=mysql_url, mongo_url=mongo_url,
                           default_username=app.config['default_username'], form=form)


@app.route('/mongo/edit/<twit_id>', methods=['GET', 'POST'])
def edit_twit_mongo(twit_id):
    db = app.config['dbHelper_mongo']
    form = TwitForm()
    twit = db.get_a_twit(twit_id)

    if form.validate_on_submit():
        twit = form.twit.data
        db.update_a_twit(twit, twit_id)
        return redirect(url_for('show_twits_mongo'))

    return render_template('edit_twit.html', type='mongo', twit=twit, form=form)


@app.route('/mongo/delete/<twit_id>')
def delete_twit_mongo(twit_id):
    app.config['dbHelper_mongo'].delete_a_twit(twit_id)
    return redirect(url_for('show_twits_mongo'))


@app.route('/mysql', methods=['GET', 'POST'])
def show_twits_mysql():
    # If a new twit is submitted
    db = app.config['dbHelper_mysql']
    form = TwitForm()

    if form.validate_on_submit():
        twit = form['twit'].data
        db.add_a_new_twit(twit)

    twits = db.get_all_twits()
    mysql_url = url_for('show_twits_mysql')
    mongo_url = url_for('show_twits_mongo')

    return render_template('show_twits.html', twits=twits, type='mysql', mysql_url=mysql_url, mongo_url=mongo_url,
                           default_username=app.config['default_username'], form=form)


@app.route('/mysql/edit/<twit_id>', methods=['GET', 'POST'])
def edit_twit_mysql(twit_id):
    db = app.config['dbHelper_mysql']
    form = TwitForm()
    twit = db.get_a_twit(twit_id)

    if form.validate_on_submit():
        twit = form.twit.data
        db.update_a_twit(twit_id, twit)
        return redirect(url_for('show_twits_mysql'))

    return render_template('edit_twit.html', type='mysql', twit=twit, form=form)


@app.route('/mysql/delete/<twit_id>')
def delete_twit_mysql(twit_id):
    app.config['dbHelper_mysql'].delete_twit(twit_id)
    return redirect(url_for('show_twits_mysql'))


if __name__ == '__main__':
    app.run(debug=True, port=4000, host='0.0.0.0')
