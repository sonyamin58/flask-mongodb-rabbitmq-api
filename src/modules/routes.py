from flask import request, jsonify, Blueprint

routes = Blueprint('routes', __name__)


@routes.route('/')
def hello():
    return jsonify({"status": True, "message": "Hello"}), 200
