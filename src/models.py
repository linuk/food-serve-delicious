from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class Users(db.Model):
    """User model"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    salt = db.Column(db.String(150), nullable=False)
    hashed = db.Column(db.String(150), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now())
    authenticated = db.Column(db.Boolean, nullable=False, default=True)
    activate = db.Column(db.Boolean, nullable=False, default=True)
    anonymous = db.Column(db.Boolean, nullable=False, default=False)
    meals = db.relationship('Meals', backref='users', lazy=True)

    def get_id(self):
        return self.id

    def is_authenticated(self):
        return self.authenticated

    def is_active(self):
        return True

    def is_anonymous(self):
        return self.anonymous


class Meals(db.Model):
    """Meal Model"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String)
    image = db.Column(db.String)
    postcode = db.Column(db.String(20), nullable=False)
    guest_num = db.Column(db.Integer, default=1)
    time = db.Column(db.Time, nullable=False)
    date = db.Column(db.Date, nullable=False)
    price = db.Column(db.Float, nullable=False, default=0)
    lat = db.Column(db.Float, nullable=False)
    lng = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    reservation_id = db.relationship('Reservations', backref='meals', lazy=True)


class Reservations(db.Model):
    """Reservation booking status"""
    id = db.Column(db.Integer, primary_key=True)
    meal_id = db.Column(db.Integer, db.ForeignKey('meals.id'), nullable=False)
    guest_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
