from flask import Flask, request, jsonify

app = Flask(__name__)


def transaction_handler(app):
    @app.route('/topup', methods=['GET'])
    def topup():
        return jsonify({
            "status": True,
            "info": "topup"
        }), 200

    @app.route('/transfer', methods=['GET'])
    def transfer():
        return jsonify({
            "status": True,
            "info": "transfer"
        }), 200

    @app.route('/pay', methods=['GET'])
    def payment():
        return jsonify({
            "status": True,
            "info": "payment"
        }), 200

    @app.route('/transactions', methods=['GET'])
    def transactions():
        return jsonify({
            "status": True,
            "info": "transactions"
        }), 200
