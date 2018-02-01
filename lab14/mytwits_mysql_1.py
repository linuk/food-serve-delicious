import pymysql
from flask import Flask, render_template
from databaseConfigs import mysqlDatabase, mysqlHost, mysqlPasssword, mysqlUsername

app = Flask(__name__)


class DBHelper:

    def __init__(self):
        self.db = pymysql.connect(
            host=mysqlHost,
            user=mysqlUsername,
            passwd=mysqlPasssword,
            db=mysqlDatabase
        )

    def get_all_twits(self):
        query = 'SELECT u.username, t.twit, t.created_at FROM twits t, users u WHERE t.user_id=u.user_id ORDER BY t.created_at ASC '
        with self.db.cursor() as cursor:
            cursor.execute(query)
            return cursor.fetchall()


@app.route('/')
def index():
    dbHelper = DBHelper()
    twits = dbHelper.get_all_twits()
    page_title = 'Read Twits from MySql Database'
    body_title = page_title
    template = 'twits_mysql.html'

    return render_template(template, page_title=page_title, body_title=body_title, twits=twits)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=4000)
