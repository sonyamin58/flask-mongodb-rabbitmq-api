from flask import jsonify, Blueprint
from datetime import datetime

routes = Blueprint('routes', __name__)


@routes.route('/')
def index():
    now = datetime.now()

    return jsonify({
        "status": True,
        "message": "Hello World",
        "datetime": now
    }), 200
