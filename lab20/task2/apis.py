from flask import request
from flask_restful import Resource, reqparse, fields, marshal_with
from models import db, Twits, Users

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
        return Twits.query.filter_by(twit_id=twit_id).first()

    @marshal_with(response_fields)
    def post(self):
        try:
            args = parser.parse_args()
            db.session.add(Twits(user_id=args['user_id'], twit=args['twit']))
            db.session.commit()
            return {'success': True}
        except Exception:
            return {'success': False}

    @marshal_with(response_fields)
    def put(self, twit_id):
        try:
            twit = Twits.query.filter_by(twit_id=twit_id).first()
            twit.twit = request.form['twit']
            db.session.commit()
            return {'success': True}
        except:
            return {'success': False}

    @marshal_with(response_fields)
    def delete(self, twit_id):
        try:
            db.session.delete(Twits.query.filter_by(twit_id=twit_id).first())
            db.session.commit()
            return {'success': True}
        except:
            return {'success': False}


class UsersApi(Resource):
    @marshal_with(resource_fields)
    def get(self, user_id):
        return Users.query.filter_by(user_id=user_id)


class UsersTwitsApi(Resource):
    @marshal_with(resource_fields)
    def get(self, user_id):
        return Users.query.filter_by(user_id=user_id).first().twits


# Customised functions
def api_route(endpoint: str):
    return api_route_base + endpoint
