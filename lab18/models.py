from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class Users(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String, nullable=False)
    salt = db.Column(db.String(150), nullable=True)
    hashed = db.Column(db.String(150), nullable=True)
    twits = db.relationship('Twits', backref='user', lazy=True)

    def get_id(self):
        return self.user_id

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False


class Twits(db.Model):
    twit_id = db.Column(db.Integer, primary_key=True)
    twit = db.Column(db.String, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now())
