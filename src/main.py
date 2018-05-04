from flask import Flask
from credentials import APP_SECRET_KEY, SQLALCHEMY_DATABASE_URI, GOOGLE_MAP_API_KEY
from flask_restful import Api
from models import db
from APIs import UserAPI, MealsAPI, ReservationsAPI, api_route
from auth.auth_blueprint import auth_blueprint
from meals.meals_blueprint import meals_blueprint
from flask_googlemaps import GoogleMaps

app = Flask(__name__)
app.secret_key = APP_SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.register_blueprint(auth_blueprint)
app.register_blueprint(meals_blueprint)

GoogleMaps(app, key=GOOGLE_MAP_API_KEY)

db.init_app(app)

api = Api(app)
api.add_resource(UserAPI, api_route('users/<int:user_id>'), api_route('users'))
api.add_resource(MealsAPI, api_route('meals/<int:meal_id>'), api_route('meals'))
api.add_resource(ReservationsAPI, api_route('reservations/<int:reservation_id>'), api_route('reservations'))

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=4000)
