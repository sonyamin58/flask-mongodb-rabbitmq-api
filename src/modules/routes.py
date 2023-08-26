from flask import jsonify, Blueprint
from datetime import datetime
from bson.json_util import dumps, loads

from src.config.mongo import db
from src.modules.v1.auth.auth_handler import auth_handler
from src.modules.v1.transaction.transaction_handler import transaction_handler

routes = Blueprint('routes', __name__)
auth_handler(routes)
transaction_handler(routes)


@routes.route('/')
def index():
    now = datetime.now()

    return jsonify({
        "status": True,
        "message": "Hello World",
        "datetime": now
    }), 200
