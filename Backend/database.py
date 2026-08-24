from pymongo import MongoClient

MONGO_URI = "mongodb://localhost:27017"
DATABASE_NAME = "ecommerceDB"

client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]


def test_connection():
    return client.admin.command("ping")
