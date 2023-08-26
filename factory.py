from flask import Flask
from flask_cors import CORS
from src.modules.routes import routes


def build():
    app = Flask(__name__)

    CORS(app, resources={r"/*": {"origins": "*"}})

    app.register_blueprint(routes, url_prefix='/')

    return app
