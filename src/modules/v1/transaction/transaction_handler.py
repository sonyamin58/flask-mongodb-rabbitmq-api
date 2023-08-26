from flask import Blueprint, request, jsonify
from uuid import uuid4, UUID
from flask_jwt_extended import get_current_user, get_jwt_identity, jwt_required

from src.config.mongo import db
from src.config.rabbitmq import rabbitmq
from src.utils.const import MQ

from src.modules.v1.transaction.transaction_service import TransactionService
from src.modules.v1.auth.auth_service import AuthService

transaction_handler = Blueprint('transaction_handler', __name__)
service = TransactionService(db)


@transaction_handler.route('/topup', methods=['POST'])
@jwt_required()
def topup():
    req = request.json
    print(req)
    if (req.get('amount') == "" or req.get('amount') == None):
        return jsonify({
            "status": "FAILED",
            "message": "Please fill in the data correctly!",
        }), 422

    me = get_current_user()
    # credit (topup)
    topup_amount = req.get("amount", 0)
    balance_before = int(me["balance"])
    balance_after = int(balance_before) + int(topup_amount)
    params = {
        "topup_id": str(uuid4()),
        "user_id": str(get_jwt_identity()),
        "amount": int(topup_amount),
        "remarks": str("Topup Sebesar Rp " + topup_amount),
        "balance_before": balance_before,
        "balance_after": balance_after,
    }

    result = service.credit(params)

    if result != False:
        return jsonify({
            "status": "SUCCESS",
            "result": result
        }), 200

    return jsonify({
        "status": "FAILED",
        "msg": "Bad Request! Please try again",
    }), 400


@transaction_handler.route('/pay', methods=['POST'])
@jwt_required()
def payment():
    req = request.json
    if (
        (req.get('amount') == "" or req.get('remarks') == "") or
        (req.get('amount') == None or req.get('remarks') == None)
    ):
        return jsonify({
            "status": "FAILED",
            "message": "Please fill in the data correctly!",
        }), 422

    me = get_current_user()
    # debit (payment)
    payment_amount = req.get("amount", 0)
    payment_remarks = req.get("remarks", "")
    balance_before = int(me["balance"])
    balance_after = int(balance_before) - int(payment_amount)
    if balance_after < 0:
        return jsonify({
            "status": "FAILED",
            "message": "Balance is not enough!",
        }), 400

    params = {
        "topup_id": str(uuid4()),
        "user_id": str(get_jwt_identity()),
        "amount": int(payment_amount),
        "remarks": str(payment_remarks),
        "balance_before": balance_before,
        "balance_after": balance_after,
    }

    result = service.debit(params)

    if result != False:
        return jsonify({
            "status": "SUCCESS",
            "result": result
        }), 200

    return jsonify({
        "status": "FAILED",
        "msg": "Bad Request! Please try again",
    }), 400


@transaction_handler.route('/transfer', methods=['POST'])
@jwt_required()
def transfer():
    req = request.json
    if (
        (req.get('amount') == "" or req.get('remarks') == "") or
        (req.get('target_user') == None or req.get('target_user') == None)
    ):
        return jsonify({
            "status": "FAILED",
            "message": "Please fill in the data correctly!",
        }), 422

    me = get_current_user()
    # debit (transfer)
    transfer_amount = req.get("amount", 0)
    transfer_remarks = req.get("remarks", "")
    target_user_id = req.get("target_user", "")
    balance_before = int(me["balance"])
    balance_after = int(balance_before) - int(transfer_amount)
    if balance_after < 0:
        return jsonify({
            "status": "FAILED",
            "message": "Balance is not enough!",
        }), 400

    auth_service = AuthService(db)
    target_user = auth_service.who(target_user_id)
    if target_user == False:
        return jsonify({
            "status": "FAILED",
            "message": "Target user not found!",
        }), 400

    params = {
        "transfer_id": str(uuid4()),
        "user_id": str(get_jwt_identity()),
        "target_user_id": str(target_user_id),
        "amount": int(transfer_amount),
        "remarks": str(transfer_remarks),
        "balance_before": balance_before,
        "balance_after": balance_after,
    }

    result = service.debit(params)

    if result != False:
        params["job"] = MQ["job"]["transfer_received"]
        # publish
        rabbitmq.publish(MQ["queue"]["transfer"], params)

        return jsonify({
            "status": "SUCCESS",
            "result": result
        }), 200

    return jsonify({
        "status": "FAILED",
        "msg": "Bad Request! Please try again",
    }), 400


@transaction_handler.route('/transactions', methods=['GET'])
@jwt_required()
def transactions():
    req = request.args

    # debit (payment)
    where = [
        {
            "user_id": get_jwt_identity()
        }
    ]
    if req.get("transaction_type", "") != "":
        where.append({
            "transaction_type": req.get("transaction_type", "")
        })

    result = service.history(where)

    if result != False:
        return jsonify({
            "status": "SUCCESS",
            "result": result
        }), 200

    return jsonify({
        "status": "FAILED",
        "msg": "Bad Request! Please try again",
    }), 400
