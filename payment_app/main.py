from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import requests
from pymongo import MongoClient

app = FastAPI()

# MongoDB connection
client = MongoClient("mongodb://mongodb:27017")  # Assuming MongoDB is running in a container named "mongo"
db = client["payments"]
collection = db["payments"]

class Payment(BaseModel):
    user_id: int
    order_id: int
    amount: float

@app.post("/payments")
def create_payment(payment: Payment):
    # Check if user exists
    user_url = f"http://user-app:8000/users/{payment.user_id}"
    user_response = requests.get(user_url)
    if user_response.status_code != 200:
        return JSONResponse(status_code=404, content={"detail": f"User with ID {payment.user_id} not found"})

    # Check if order exists
    order_url = f"http://order-app:8001/orders/{payment.user_id}"
    order_response = requests.get(order_url)
    if order_response.status_code != 200:
        return JSONResponse(status_code=404, content={"detail": f"Order with ID {payment.user_id} not found"})
    else:
        json = order_response.json()
        if json['order_id'] != payment.order_id:
            return JSONResponse(status_code=400, content={"detail": f"No Order with ID {payment.order_id} found for user {payment.user_id}"})

    # Check if payment with same order_id already exists
    existing_payment = collection.find_one({"order_id": payment.order_id})
    if existing_payment:
        return JSONResponse(status_code=400, content={"detail": f"Payment for Order with ID {payment.order_id} already exists"})
    
    # Create payment logic here
    payment_data = {
        "user_id": payment.user_id,
        "order_id": payment.order_id,
        "amount": payment.amount
    }
    collection.insert_one(payment_data)

    return {"message": "Payment created successfully"}

@app.get("/payments/{user_id}")
def get_payment(user_id: int):
    payment = collection.find_one({"user_id": user_id})
    print(payment)
    if payment:
        del payment['_id']
        return payment
    else:
        return JSONResponse(status_code=404, content={"detail": f"Payment with ID {user_id} not found"})