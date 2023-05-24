from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pymongo import MongoClient
import requests

app = FastAPI()

# Set up the MongoDB connection
client = MongoClient("mongodb://mongodb:27017")
db = client["orders"]
collection = db["orders"]

# API endpoint to create a user
@app.post("/orders/{user_id}")
def add_order(user_id: str, order_id: int, order_details: str):
    try:
        # Retrieve user data from the user app
        user_app_url = f"http://user-app:8000/users/{user_id}"
        response = requests.get(user_app_url)
        if response.status_code == 200:
            user_data = response.json()

            # Insert order into the MongoDB orders collection
            order = {
                "user_id": user_id,
                "order_id": order_id,
                "user_name": user_data["name"],
                "order_details": order_details
            }
            collection.insert_one(order)

            return {"detail": "Order added successfully"}
        else:
            return JSONResponse(content={"detail": "User not found"}, status_code=404)
    except:
        return JSONResponse(content={"detail": "Internal Server Error"}, status_code=500)

# API endpoint to get all users
@app.get("/orders/{user_id}")
def get_orders(user_id: str):
    try:
        # Retrieve user data from the user app
        user_app_url = f"http://user-app:8000/users/{user_id}"
        response = requests.get(user_app_url)
        if response.status_code == 200:
            user_data = response.json()

            # Retrieve orders for the user from the MongoDB orders collection
            orders = collection.find({"user_id": user_id})
            if orders.count() > 0:
                order_list = []
                for order in orders:
                    order_list.append(order['order_details'])
                return {"user_id": user_id, "user_name": user_data["name"], "order_id": order['order_id'], "orders": order_list}
            else:
                return JSONResponse(content={"detail": "No Orders"}, status_code=400)
        else:
            return JSONResponse(content={"detail": "User not found"}, status_code=404)
    except:
        return JSONResponse(content={"detail": "Internal Server Error"}, status_code=500)