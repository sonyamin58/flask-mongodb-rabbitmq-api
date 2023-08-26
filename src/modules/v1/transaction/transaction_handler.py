from flask import Blueprint, request, jsonify

transaction_handler = Blueprint('transaction_handler', __name__)


@transaction_handler.route('/topup', methods=['GET'])
def topup():
    return jsonify({
        "status": True,
        "info": "topup"
    }), 200


@transaction_handler.route('/transfer', methods=['GET'])
def transfer():
    return jsonify({
        "status": True,
        "info": "transfer"
    }), 200


@transaction_handler.route('/pay', methods=['GET'])
def payment():
    return jsonify({
        "status": True,
        "info": "payment"
    }), 200


@transaction_handler.route('/transactions', methods=['GET'])
def transactions():
    return jsonify({
        "status": True,
        "info": "transactions"
    }), 200
