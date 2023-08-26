from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, get_current_user, get_jwt_identity, jwt_required

from src.config.mongo import db
from src.modules.v1.auth.auth_service import AuthService

auth_handler = Blueprint('auth_handler', __name__)
service = AuthService(db)


@auth_handler.route('/register', methods=['POST'])
def register():
    req = request.json
    if (
        req.get('first_name') == "" or req.get('last_name') == "" or req.get(
            'phone_number') == "" or req.get('pin') == ""
    ) or (
        req.get('first_name') == None or req.get('last_name') == None or req.get(
            'phone_number') == None or req.get('pin') == None
    ):
        return jsonify({
            "status": "FAILED",
            "message": "Please fill in the data correctly!",
        }), 422

    # save data
    result = service.signup()

    if result != False:
        return jsonify({
            "status": "SUCCESS",
            "result": result
        }), 200

    return jsonify({
        "status": "FAILED",
        "msg": "Phone Number already registered",
    }), 400


@auth_handler.route('/login', methods=['POST'])
def login():
    req = request.json
    if (
        req.get('phone_number') == "" or req.get('pin') == ""
    ) or (
        req.get('phone_number') == None or req.get('pin') == None
    ):
        return jsonify({
            "status": "FAILED",
            "message": "Please fill in the data correctly!",
        }), 422

    # check data
    result = service.signin()

    if result != False:
        tokens = {
            "acess_token": create_access_token(identity=result['user_id']),
            "refresh_token": create_refresh_token(identity=result['user_id'])
        }

        return jsonify({
            "status": "SUCCESS",
            "result": tokens,
        }), 200

    return jsonify({
        "status": "FAILED",
        "msg": "Phone number and pin is doesn't match",
    }), 401


@auth_handler.route('/me', methods=['GET'])
@jwt_required()
def me():
    me = get_current_user()
    return jsonify({
        "status": True,
        "info": "me",
        "result": me
    }), 200


@auth_handler.route('/profile', methods=['PUT'])
@jwt_required()
def profile():
    req = request.json

    req.pop("_id", None)
    req.pop("user_id", None)
    req.pop("balance", None)

    where = {"user_id": str(get_jwt_identity())}

    # update data
    result = service.update(where, req)

    if result != False:
        me = service.who(str(get_jwt_identity()))
        return jsonify({
            "status": "SUCCESS",
            "result": me
        }), 200

    return jsonify({
        "status": "FAILED",
        "msg": "Bad Request! Please try again",
    }), 401
