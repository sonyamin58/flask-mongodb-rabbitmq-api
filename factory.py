from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from datetime import timedelta
import os
from os.path import join, dirname
from dotenv import load_dotenv

from src.modules.v1.auth.auth_service import AuthService
from src.modules.v1.transaction.transaction_handler import transaction_handler
from src.modules.v1.auth.auth_handler import auth_handler
from src.modules.routes import routes

from src.config.mongo import db
from src.config.rabbitmq import rabbitmq
rabbitmq.connection()

# start build
dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'SECRET')
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(
    hours=int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES', 1)))
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(
    hours=int(os.getenv('JWT_REFRESH_TOKEN_EXPIRES', 1)))

jwt = JWTManager()
jwt.init_app(app)


@jwt.user_identity_loader
def user_identity_loader(me):
    # print('user_identity_loader', me)
    return me


@jwt.user_lookup_loader
def user_lookup_loader(_jwt_header, jwt_data):
    service = AuthService(db)
    me = service.who(jwt_data["sub"])
    # print('user_lookup_loader', me)
    return me


def build():
    app.register_blueprint(auth_handler, url_prefix='/')
    app.register_blueprint(transaction_handler, url_prefix='/')
    app.register_blueprint(routes, url_prefix='/')

    return app
