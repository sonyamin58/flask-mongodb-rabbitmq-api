from flask import request
from werkzeug.security import generate_password_hash, check_password_hash
from uuid import uuid4, UUID
from datetime import datetime
from bson import ObjectId


class AuthService:
    def __init__(self, db):
        self.db = db
        self.users = db.users
        self.now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def signup(self):
        req = request.json

        exist = self.users.find_one({"phone_number": req.get("phone_number")})
        if exist is None:
            self.now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            user = {
                "user_id": str(uuid4()),
                "first_name": str(req.get('first_name')),
                "last_name": str(req.get('last_name')),
                "phone_number": str(req.get('phone_number')),
                "pin": generate_password_hash(str(req.get('pin'))),
                "address": str(req.get('address') or ""),
                "balance": 0,
                "created_at": self.now,
            }

            insert = self.users.insert_one(user)
            if insert.acknowledged:
                del user['_id']
                del user['pin']
                del user['balance']
                return user

        return False

    def signin(self):
        req = request.json

        user = self.users.find_one(
            {"phone_number": req.get("phone_number")},
            {'_id': False}
        )

        if user is not None and check_password_hash(user['pin'], str(req.get("pin"))):
            return user

        return False

    def who(self, user_id):
        user = self.users.find_one(
            {"user_id": str(user_id)},
            {'_id': False, 'pin': False}
        )

        if user is not None:
            return user

        return False

    def update(self, where, set):
        self.now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        set["updated_at"] = self.now

        update = self.users.update_one(
            where,
            {"$set": set}
        )

        if update.acknowledged:
            return update

        return False
