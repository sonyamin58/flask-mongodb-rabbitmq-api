from flask import jsonify, Blueprint
from datetime import datetime

routes = Blueprint('routes', __name__)


@routes.route('/')
def index():
    now = datetime.now()

    data = {
        "a": "b",
        "b": "c"
    }
    print(data)
    del data['a']

    return jsonify({
        "status": True,
        "message": "Hello World",
        "datetime": now,
        "data": data
    }), 200
