from flask import Flask
from apis import api_route, TwitApi, UsersApi, UsersTwitsApi
from variables import app_secret_key
from flask_restful import Api
from models import db
from twits.twits_blueprint import twits_blueprint
from auth.login_blueprint import auth_blueprint

app = Flask(__name__)
app.secret_key = app_secret_key
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://mytwits_user:mytwits_password@localhost/mytwits'
app.register_blueprint(twits_blueprint)
app.register_blueprint(auth_blueprint)

db.init_app(app)

api = Api(app)
api.add_resource(TwitApi, api_route('twits/<int:twit_id>'), api_route('twits'))
api.add_resource(UsersApi, api_route('users/<int:user_id>'))
api.add_resource(UsersTwitsApi, api_route('users/<int:user_id>/twits'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=4000)
