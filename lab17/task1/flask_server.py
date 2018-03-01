from flask import Flask, jsonify
from dbHelpers import DBHelper_mysql
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)
app.secret_key = 'klahyfagloug2to871h9y0*^(*Hiyf1o3hg7936f1'

db = DBHelper_mysql()

@app.route('/api/v1/twits')
@app.route('/api/v1/twits/<username>')
def getAllTwits(username=None):
  if username:
    twits = db.get_twits_by_username(username)
    return jsonify({"twits": twits})
  else:
    twits = db.get_all_twits()
    return jsonify({"twits": twits})

@app.route('/api/v1/user/<username>')
def getUserData(username):
  data = db.get_user_by_username(username)
  return jsonify({"data": data})

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=4000, debug=True)

