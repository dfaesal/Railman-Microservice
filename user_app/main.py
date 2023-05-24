from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from pydantic import BaseModel
from bson import ObjectId
from fastapi.responses import JSONResponse

app = FastAPI()

# Set up the MongoDB connection
client = MongoClient("mongodb://mongodb:27017")
db = client["users"]
collection = db["users"]

class User(BaseModel):
    id: int
    name: str
    email: str
    address: str
    mobile: int

# API endpoint to create a user
@app.post("/users")
def create_user(user: User):
    try:
        db_user = collection.find_one({'id' : user.id})
        if(db_user):
            return JSONResponse(content={"detail": "User {user.id} already present"}, status_code=400)
        else:
            user_dict = user.dict()
            user_dict['_id'] = ObjectId()
            collection.insert_one(user_dict)
            return {f"user {user_dict['id']} created successfully"}
    except:
        return JSONResponse(content={"detail": "Internal Server Error"}, status_code=500)

# API endpoint to get all users
@app.get("/users", status_code=200)
def get_all_users():
    try:
        users = collection.find()
        user_list = []
        for user in users:
            user_data = User(**user)
            user_list.append(user_data)
        return user_list
    except:
        return JSONResponse(content={"detail": "Internal Server Error"}, status_code=500)

# API endpoint to get specific user
@app.get("/users/{u_id}")
def get_user(u_id: int):
    try:
        user = collection.find_one({"id": u_id})
        if user:
            user_data = User(**user)
            return user_data
        else:
            return JSONResponse(status_code=404, content={"detail": f"There is no User with id as {u_id}"})
    except:
        return JSONResponse(content={"detail": "Internal Server Error"}, status_code=500)