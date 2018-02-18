# /usr/bin/python3

import pymongo
from flask import Flask, render_template
from databaseConfigs import monogoDatabase, monogoTable


class DBHelper:

    def __init__(self):
        client = pymongo.MongoClient()
        self.db = client[monogoDatabase]

    def get_all_twits(self):
        """get all the twits from the database"""
        return self.db[monogoTable].find()


app = Flask(__name__)


@app.route('/')
def index():
    page_title = "Twits FromMongo"
    body_title = page_title

    dbHelper = DBHelper()
    twits = dbHelper.get_all_twits()
    template = 'twits_mongo.html'

    return render_template(template, page_title=page_title, body_title=body_title, twits=twits)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=4000)
