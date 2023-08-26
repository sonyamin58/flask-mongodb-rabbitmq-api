from flask import Flask, request, jsonify
from src.config.mongo import db
app = Flask(__name__)


def auth_handler(app):
    @app.route('/register', methods=['GET'])
    def register():
        return jsonify({
            "status": True,
            "info": "register"
        }), 200

    @app.route('/login', methods=['GET'])
    def login():
        return jsonify({
            "status": True,
            "info": "login"
        }), 200

    @app.route('/me', methods=['GET'])
    def me():
        return jsonify({
            "status": True,
            "info": "register"
        }), 200

    @app.route('/update', methods=['GET'])
    def update():
        return jsonify({
            "status": True,
            "info": "login"
        }), 200
