from pymysql import connect, cursors
from datetime import datetime

database = 'mytwits'
table = 'twits'
mysql_username = 'mytwits_user'
mysql_password = 'mytwits_password'
mysql_host = 'localhost'
default_user_id = 1
default_username = 'dan1'

class DBHelper_mysql:
  
    def __init__(self):
        self.db = connect(
            host=mysql_host,
            database=database,
            user=mysql_username,
            passwd=mysql_password,
        )

    def get_all_twits(self):
        with self.db.cursor(cursors.DictCursor) as cursor:
            query = 'SELECT u.username, t.twit, t.created_at, t.twit_id FROM twits t, users u WHERE t.user_id=u.user_id ORDER BY t.created_at DESC '
            cursor.execute(query)
            return cursor.fetchall()

    def get_a_twit(self, twit_id):
        with self.db.cursor(cursors.DictCursor) as cursor:
            query = 'SELECT u.username, t.twit, t.created_at, t.twit_id from twits t, users u WHERE twit_id={} and u.user_id=t.user_id'.format(
                twit_id)
            cursor.execute(query)
            return cursor.fetchone()

    def get_twits_by_username(self, username):
        with self.db.cursor(cursors.DictCursor) as cursor:
            query = 'SELECT u.username, t.twit, t.created_at, t.twit_id from twits t, users u WHERE u.username="{}" and u.user_id=t.user_id'.format(
                username)
            cursor.execute(query)
            return cursor.fetchall()

    def get_user_by_username(self, username):
        with self.db.cursor(cursors.DictCursor) as cursor:
            query = 'SELECT * FROM users u WHERE u.username="{}"'.format(username)
            print(query)
            cursor.execute(query)
            return cursor.fetchone()

    def add_a_new_twit(self, twit, user_id):
        with self.db.cursor(cursors.DictCursor) as cursor:
            query = 'INSERT INTO twits (twit, user_id) VALUES("{}", "{}")'.format(twit, user_id)
            cursor.execute(query)
            return self.db.commit()

    def update_a_twit(self, twit_id, twit):
        with self.db.cursor(cursors.DictCursor) as cursor:
            query = 'UPDATE twits SET twit="{}", created_at="{}" WHERE twit_id={}'.format(twit, datetime.utcnow(),
                                                                                          twit_id)
            print(query)
            cursor.execute(query)
            return self.db.commit()

    def delete_twit(self, twit_id):
        with self.db.cursor(cursors.DictCursor) as cursor:
            query = 'DELETE FROM twits WHERE twit_id = {}'.format(twit_id)
            cursor.execute(query)
            return self.db.commit()