from pymongo import MongoClient

# Secret key for JWT
SECRET_KEY = 'mysecret'

# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client.Business  # Your database name

# Collections
users = db.users       # Users collection
biz = db.biz           # Businesses collection (matches your seed_all.py)
operations = db.operations
blacklist = db.blacklist
