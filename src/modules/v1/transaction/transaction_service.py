from flask import request
from datetime import datetime


class TransactionService:
    def __init__(self, db):
        self.db = db
        self.users = db.users
        self.transactions = db.transactions
        self.now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def credit(self, params):
        params["transaction_type"] = str("CREDIT")

        return self.insert(params)

    def debit(self, params):
        params["transaction_type"] = str("DEBIT")

        return self.insert(params)

    def insert(self, params):
        self.now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        params["created_at"] = self.now

        if params.get("target_user_id") is not None:
            params["status"] = str("PENDING")
        else:
            params["status"] = str("SUCCESS")

        print('transaction', params)
        insert = self.transactions.insert_one(params)
        update_balance = self.users.update_one(
            {
                "user_id": params["user_id"]
            },
            {
                "$set": {
                    "balance": params["balance_after"]
                }
            }
        )
        if insert.acknowledged and update_balance.acknowledged:
            del params['_id']
            del params['user_id']
            del params['transaction_type']
            del params['status']

            return params

        return False

    def history(self, where):
        history = list(self.transactions.find(
            {"$and": where},
            {'_id': False}
        ))

        return history

    def update_status(self, where, status):
        success = self.transactions.update_one(
            where,
            {
                "$set": {
                    "status": status
                }
            }
        )
        if success.acknowledged:
            return success

        return False
