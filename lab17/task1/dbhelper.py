import hashlib, random, pymysql, string
from variables import mysqlDatabase, mysqlHost, mysqlPasssword, mysqlUsername
from flask import escape
from datetime import datetime


class DBHelper:

    def __init__(self):
        self.db = pymysql.connect(
            host=mysqlHost,
            user=mysqlUsername,
            passwd=mysqlPasssword,
            db=mysqlDatabase,
            cursorclass=pymysql.cursors.DictCursor
        )

    def execute(self, query, type='all'):

        try:
            with self.db.cursor() as cursor:
                cursor.execute(query)
        except:
            self.db.rollback()
            return None

        if type == 'one':
            return cursor.fetchone()
        if type == 'all':
            return cursor.fetchall()
        if type == 'commit':
            return self.db.commit()

        self.db.close()

    def get_all_twits(self, user_id):
        query = 'SELECT t.created_at, t.twit_id, t.twit, t.created_at FROM twits t WHERE t.user_id = "%s" ORDER BY t.created_at ASC' % escape(
            user_id)
        return self.execute(query, 'all')

    def get_user(self, user_id):
        query = 'SELECT * FROM users WHERE user_id = "{}"'.format(user_id)
        return self.execute(query, 'one')

    # return user_id as the first element in the result tuple
    def get_user_id_by_username_and_password(self, username, password):
        query = 'SELECT user_id FROM users WHERE username = "%s" AND password = "%s"' % (
            escape(username), escape(password))
        return self.execute(query, 'one')

    def add_user(self, username, password):
        salt = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(32)])
        hashed = hashlib.sha512((salt + password).encode('utf-8')).hexdigest()
        query = 'INSERT INTO users (username, password, salt, hashed) VALUES ("{}", "{}", "{}", "{}")'.format(
            escape(username), escape(password), salt, hashed)
        return self.execute(query, 'commit')

    def get_a_twit(self, twit_id):
        query = 'SELECT t.twit FROM twits t WHERE t.twit_id="{}"'.format(twit_id)
        return self.execute(query, 'one')

    def add_a_new_twit(self, user_id, twit):
        query = 'INSERT INTO twits (twit, user_id, created_at) VALUES ("{}", "{}", "{}")'.format(escape(twit), user_id,
                                                                                                 datetime.utcnow())
        return self.execute(query, 'commit')

    def update_a_twit(self, twit_id, twit):
        query = 'UPDATE twits SET twit="{}", created_at="{}" WHERE twit_id={}'.format(escape(twit), datetime.utcnow(),
                                                                                      twit_id)
        return self.execute(query, 'commit')

    def delete_twit(self, twit_id):
        query = 'DELETE FROM twits WHERE twit_id="{}"'.format(twit_id)
        return self.execute(query, 'commit')

    def check_password(self, username, password):
        query = 'SELECT user_id, salt, hashed FROM users WHERE username="{}"'.format(username)
        user = self.execute(query, 'one')
        if user:
            user_id, salt, hashed = user['user_id'], user['salt'], user['hashed']
            return user_id if hashlib.sha512((salt + password).encode('utf-8')).hexdigest() == hashed else None
