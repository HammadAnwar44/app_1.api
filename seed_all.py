import bcrypt
import globals
from dummyDATA import dummyDATA

users = globals.db.users
biz_collection = globals.db.biz

# --------------------------------- Seed Users with Roles -----------------------------------
user_list = [
    {
        "name": "Ali Khan",
        "username": "ali",
        "password": "ali123",
        "email": "ali@nearbyservices.co.uk",
        "admin": False,
        "role": "employee"
    },
    {
        "name": "Sarah Malik",
        "username": "sarah",
        "password": "sarah123",
        "email": "sarah@nearbyservices.co.uk",
        "admin": False,
        "role": "client"
    },
    {
        "name": "Administrator",
        "username": "admin",
        "password": "admin123",
        "email": "admin@company.com",
        "admin": True,
        "role": "admin"
    }
]

# --------------------------------- Clear existing users ----------------------------------

users.delete_many({})

#------------------------------------ Insert new users ------------------------------------

for user in user_list:
    hashed_pw = bcrypt.hashpw(user["password"].encode("utf-8"), bcrypt.gensalt())
    users.insert_one({
        "name": user["name"],
        "username": user["username"],
        "password": hashed_pw,
        "email": user["email"],
        "admin": user["admin"],
        "role": user["role"]
    })

print("Users seeded successfully!")


biz_data = dummyDATA()
biz_collection.delete_many({})  
biz_collection.insert_many(biz_data)

print(f" {len(biz_data)} business records seeded successfully!")
