from flask import request, jsonify
from flask_restful import Resource, reqparse, fields, marshal_with
from dbhelper import DBHelper

db = DBHelper()
api_route_base = '/api/v1/'

# Data Parsers
parser = reqparse.RequestParser()
parser.add_argument('twit', type=str, help='text of the twit; must be a string')
parser.add_argument('twit_id', type=int, help='id of the twit; must be a integer')
parser.add_argument('user_id', type=int, help='id of the user; must be a integer')

# Resource type validators
resource_fields = {
    'twit_id': fields.Integer,
    'twit': fields.String,
    'user_id': fields.Integer,
    'created_at': fields.DateTime(dt_format='rfc822')
}

response_fields = {
    'success': fields.Boolean
}


# APIs
class TwitApi(Resource):
    @marshal_with(resource_fields)
    def get(self, twit_id):
        return db.get_a_twit(twit_id)

    @marshal_with(response_fields)
    def post(self):
        try:
            args = parser.parse_args()
            twit = args['twit']
            user_id = args['user_id']
            db.add_a_new_twit(user_id, twit)
            return {'success': True}
        except Exception:
            return {'success': False}

    @marshal_with(response_fields)
    def put(self, twit_id):
        try:
            twit = request.form['twit']
            db.update_a_twit(twit_id, twit)
            return {'success': True}
        except:
            return {'success': False}

    @marshal_with(response_fields)
    def delete(self, twit_id):
        try:
            print(db.delete_twit(twit_id))

            return {'success': True}
        except:
            return {'success': False}


class UsersApi(Resource):
    @marshal_with(resource_fields)
    def get(self, user_id):
        return db.get_user(user_id)


class UsersTwitsApi(Resource):
    @marshal_with(resource_fields)
    def get(self, user_id):
        return jsonify(db.get_all_twits(user_id))


# Customised functions
def api_route(endpoint: str):
    return api_route_base + endpoint
