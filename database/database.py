from flask import Blueprint, request
from flask_login import login_user, logout_user, LoginManager
from models import Users, Meals, Reservations
from APIs import api_route, UserAPI, MealsAPI, ReservationsAPI

database_blueprint = Blueprint('database_blueprint', __name__)
login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id):
    return Users.query.filter_by(id=user_id)


@database_blueprint.record_once
def on_load(state):
    login_manager.init_app(state.app)


