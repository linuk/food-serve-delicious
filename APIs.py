from flask_restful import Resource, fields, marshal_with, reqparse
from models import db, Users, Meals, Reservations
from passwordhelper import PasswordHelper
from datetime import datetime
import urllib3
import json

ph = PasswordHelper()
api_route_base = '/api/v1/'
postcode_api_url = 'https://api.postcodes.io/postcodes/'


class UserAPI(Resource):
    resource_fields = {
        'id': fields.Integer,
        'username': fields.String,
        'email': fields.String,
        'salt': fields.String,
        'hashed': fields.String,
        'created_at': fields.DateTime,
        'authenticated': fields.Boolean,
        'activate': fields.Boolean,
        'anonymous': fields.Boolean,
        'meals': fields.String,
    }

    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, help='username must be a string')
    parser.add_argument('email', type=str, help='email must be a string')
    parser.add_argument('password', type=str, help='password must be a string')

    @marshal_with(resource_fields)
    def get(self, user_id=None):
        if user_id is None:
            return Users.query.all()
        return Users.query.filter_by(id=user_id).first()

    def post(self):
        args = self.parser.parse_args()
        salt = PasswordHelper.get_salt()
        password = args['password']
        hashed = PasswordHelper.get_hash((salt + password).encode('utf-8'))
        created_at = datetime.now()
        db.session.add(Users(username=args['username'],
                             email=args['email'],
                             salt=salt,
                             hashed=hashed,
                             created_at=created_at))
        db.session.commit()
        return True

    def put(self, user_id):
        user = Users.query.filter_by(id=user_id)
        if user is None:
            return False
        else:
            args = self.parser.parse_args()
            if args['username'] is not None:
                user.username = args['username']

            if args['password'] is not None:
                salt = user.salt
                user.hash = PasswordHelper.get_hash((salt + args['password']).encode('utf-8'))

            if args['email'] is not None:
                user.email = args['email']
        db.session.commit()
        return True

    def delete(self, user_id):
        db.session.delete(Users.query.filter_by(id=user_id))
        return True


class MealsAPI(Resource):
    resource_fields = {
        'id': fields.Integer,
        'name': fields.String,
        'description': fields.String,
        'image': fields.String,
        'guest_num': fields.Integer,
        'time': fields.DateTime,
        'price': fields.Float,
        'lat': fields.Float,
        'lng': fields.Float,
    }

    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, help='name must be a string.')
    parser.add_argument('description', type=str, help='description must be a string.')
    parser.add_argument('image', type=str, help='image must be a string.')
    parser.add_argument('guest_num', type=int, help='guest_num must be an integer.')
    parser.add_argument('time', type=datetime, help='time must be a datetime.')
    parser.add_argument('price', type=float, help='price must be a float number.')
    parser.add_argument('lat', type=float, help='lat must be a float number.')
    parser.add_argument('lng', type=float, help='lng must be a float number.')

    @marshal_with(resource_fields)
    def get(self, meal_id=None):
        if meal_id is None:
            return Meals.query.all()
        return Meals.query.filter_by(id=meal_id).first()

    def post(self):
        args = self.parser.parse_args()
        db.session.add(Meals(name=args['name'],
                             description=args['description'],
                             image=args['image'],
                             guest_num=args['guest_num'],
                             time=args['time'],
                             price=args['price'],
                             lat=args['lat'],
                             lng=args['lng']))
        db.session.commit()
        return True

    def put(self, meal_id):
        args = self.parser.parse_args()
        meal = Meals.query.filter_by(id=meal_id).first()
        meal.name = args['name']
        meal.description = args['description']
        meal.image = args['image']
        meal.guest_num = args['guest_num']
        meal.time = args['time']
        meal.price = args['price']
        meal.lat = args['lat']
        meal.lng = args['lng']
        db.session.commit()
        return True

    def delete(self, meal_id):
        db.session.delete(Meals.query.filter_by(id=meal_id).first())
        db.session.commit()
        return True


class ReservationsAPI(Resource):
    resource_fields = {
        'meal_id': fields.Integer,
        'guest_id': fields.Integer
    }

    parser = reqparse.RequestParser()
    parser.add_argument('meal_id', type=int, help='meal id must be an integer')
    parser.add_argument('guest_id', type=int, help='guest id must be an integer')

    @marshal_with(resource_fields)
    def get(self, reservation_id=None):
        if reservation_id is None:
            return Reservations.query.all()
        return Reservations.query.filter_by(id=reservation_id).first()

    def post(self):
        args = self.parser.parse_args()
        db.session.add(Reservations(meal_id=args['meal_id'], guest_id=args['guest_id']))
        db.session.commit()
        return True

    def put(self, reservation_id):
        args = self.parser.parse_args()
        reservation = Reservations.query.filter_by(id=reservation_id)
        reservation['meal_id'] = args['meal_id']
        reservation['guest_id'] = args['guest_id']
        db.session.commit()
        return True

    def delete(self, reservation_id):
        db.session.delete(Reservations.query.filter_by(id=reservation_id))
        db.session.commit()
        return True


# Customised functions
def api_route(endpoint: str):
    return api_route_base + endpoint


def fetch_postcode(postcode):
    """Fetch postcode details, reference: https://postcodes.io"""
    http = urllib3.PoolManager()
    res = http.request('GET', postcode_api_url + postcode)
    return [res.status, json.loads(res.data.decode("utf-8"))]
