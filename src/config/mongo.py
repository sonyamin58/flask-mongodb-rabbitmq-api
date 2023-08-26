import os
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError, ConnectionFailure


def mongo():
    load_dotenv()

    MONGO_INITDB_HOSTNAME = os.getenv('MONGO_INITDB_HOSTNAME')
    MONGO_INITDB_PORT = int(os.getenv('MONGO_INITDB_PORT'))
    MONGO_INITDB_DATABASE = os.getenv('MONGO_INITDB_DATABASE')
    MONGO_INITDB_USERNAME = os.getenv('MONGO_INITDB_USERNAME')
    MONGO_INITDB_PASSWORD = os.getenv('MONGO_INITDB_PASSWORD')

    try:
        client = MongoClient(
            host=f"{MONGO_INITDB_HOSTNAME}:{MONGO_INITDB_PORT}",
            username=MONGO_INITDB_USERNAME,
            password=MONGO_INITDB_PASSWORD,
            serverSelectionTimeoutMS=2000
        )
        db = client[f"{MONGO_INITDB_DATABASE}"]
        db.command('ping')

        print(" [*] MongoDB OK")

    except Exception as err:
        print("MongoDB Error:", err)
        exit(1)

    return db


db = mongo()
