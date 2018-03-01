from flask import Flask, jsonify
from dbHelpers import DBHelper_mysql
from flask_restful import Resource, Api, marshal_with, fields, reqparse

app = Flask(__name__)
api = Api(app)
app.secret_key = 'klahyfagloug2to871h9y0*^(*Hiyf1o3hg7936f1'

db = DBHelper_mysql()

twit_fields = {
      'twit_id': fields.Integer,
      'twit': fields.String,
      'created_at': fields.DateTime(dt_format='rfc822')
}

class Twits(Resource):
  @marshal_with(twit_fields)
  def get(self, username = None):
    if username:
      return db.get_twits_by_username(username)
    else:
      return db.get_all_twits()

class User(Resource):
  def get(self, username):
    return jsonify({"data": db.get_user_by_username(username)})

api.add_resource(Twits, '/api/v1/twits', '/api/v1/twits/<string:username>')
api.add_resource(User, '/api/v1/user/<string:username>')

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=4000, debug=True)

