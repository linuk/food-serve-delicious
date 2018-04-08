import pymysql
from variables import mysqlDatabase, mysqlHost, mysqlPasssword, mysqlUsername
from flask import escape


class DBHelper:

    def __init__(self):
        self.db = pymysql.connect(
            host=mysqlHost,
            user=mysqlUsername,
            passwd=mysqlPasssword,
            db=mysqlDatabase
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
        if type == 'storage':
            return self.db.commit()

        self.db.close()

    def get_all_twits(self, user_id):
        query = 'SELECT t.twit, t.created_at FROM twits t WHERE t.user_id = "%s" ORDER BY t.created_at ASC' % escape(
            user_id)
        return self.execute(query, 'all')

    # return user_id as the first element in the result tuple
    def get_user_id_by_username_and_password(self, username, password):
        query = 'SELECT user_id FROM users WHERE username = "%s" AND password = "%s"' % (
            escape(username), escape(password))
        return self.execute(query, 'one')

    def add_user(self, username, password):
        query = 'INSERT INTO users (username, password) VALUES ("%s", "%s")' % (escape(username), escape(password))
        return self.execute(query, 'storage')
