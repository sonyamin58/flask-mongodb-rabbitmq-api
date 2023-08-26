from flask import Flask
import os
from dotenv import load_dotenv

from src.modules.routes import routes


def build():
    load_dotenv()

    app = Flask(__name__)
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')

    app.register_blueprint(routes, url_prefix='/')

    return app
