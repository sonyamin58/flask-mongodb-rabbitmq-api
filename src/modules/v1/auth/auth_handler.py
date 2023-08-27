from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, get_current_user, get_jwt_identity, jwt_required
from marshmallow import Schema, fields, ValidationError

from src.config.mongo import db
from src.modules.v1.auth.auth_service import AuthService

auth_handler = Blueprint('auth_handler', __name__)
service = AuthService(db)


class RegisSchema(Schema):
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)
    phone_number = fields.String(required=True)
    pin = fields.Integer(required=True)
    address = fields.String(required=False)


class LoginSchema(Schema):
    phone_number = fields.String(required=True)
    pin = fields.Integer(required=True)


class UpdateSchema(Schema):
    first_name = fields.String(required=False)
    last_name = fields.String(required=False)
    phone_number = fields.String(required=False)
    pin = fields.Integer(required=False)
    address = fields.String(required=False)


@auth_handler.route('/register', methods=['POST'])
def register():
    schema = RegisSchema()
    try:
        req = request.json
        validation = schema.load(req)

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

    except ValidationError as e:
        return jsonify({
            "status": "FAILED",
            "message": e.messages,
        }), 400

    except Exception as e:
        return jsonify({
            "status": "FAILED",
            "msg": e,
        }), 500


@auth_handler.route('/login', methods=['POST'])
def login():
    schema = LoginSchema()
    try:
        req = request.json
        validation = schema.load(req)

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

    except ValidationError as e:
        return jsonify({
            "status": "FAILED",
            "message": e.messages,
        }), 400

    except Exception as e:
        return jsonify({
            "status": "FAILED",
            "msg": e,
        }), 500


@auth_handler.route('/me', methods=['GET'])
@jwt_required()
def me():
    try:
        me = get_current_user()
        return jsonify({
            "status": True,
            "info": "me",
            "result": me
        }), 200

    except Exception as e:
        return jsonify({
            "status": "FAILED",
            "msg": e,
        }), 500


@auth_handler.route('/profile', methods=['PUT'])
@jwt_required()
def profile():
    schema = UpdateSchema()
    try:
        req = request.json

        req.pop("_id", None)
        req.pop("user_id", None)
        req.pop("balance", None)

        validation = schema.load(req)

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

    except ValidationError as e:
        return jsonify({
            "status": "FAILED",
            "message": e.messages,
        }), 400

    except Exception as e:
        return jsonify({
            "status": "FAILED",
            "msg": e,
        }), 500
