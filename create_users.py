import bcrypt
import globals

# MongoDB users collection
users = globals.users  

# User list to create
user_list = [
    {"name": "Administrator", "username": "admin", "password": "admin123", "email": "admin@company.com", "admin": True},
    {"name": "Ali Khan", "username": "ali", "password": "ali123", "email": "ali@nearbyservices.co.uk", "admin": False},
    {"name": "Sarah Malik", "username": "sarah", "password": "sarah123", "email": "sarah@nearbyservices.co.uk", "admin": False},
    {"name": "Hammad Anwar", "username": "hammad", "password": "hammad123", "email": "hammad@nearbyservices.co.uk", "admin": False},
    {"name": "Ahmed Raza", "username": "ahmed", "password": "ahmed123", "email": "ahmed@nearbyservices.co.uk", "admin": False},
    {"name": "Ayesha Khan", "username": "ayesha", "password": "ayesha123", "email": "ayesha@nearbyservices.co.uk", "admin": False},
]

# Insert users if not exist
for user in user_list:
    if not users.find_one({"username": user["username"]}):
        hashed_pw = bcrypt.hashpw(user["password"].encode("utf-8"), bcrypt.gensalt())
        users.insert_one({
            "name": user["name"],
            "username": user["username"],
            "password": hashed_pw,
            "email": user["email"],
            "admin": user["admin"]
        })
        print(f"✅ User created: {user['username']}")
    else:
        print(f"⚠️ User already exists: {user['username']}")

print("✅ User creation script completed!")
