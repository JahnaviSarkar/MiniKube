import os
from datetime import datetime
from flask import Flask, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)

# MongoDB configuration from environment variables
MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017/")
MONGO_USERNAME = os.environ.get("MONGO_USERNAME")
MONGO_PASSWORD = os.environ.get("MONGO_PASSWORD")
MONGO_AUTH_SOURCE = os.environ.get("MONGO_AUTH_SOURCE", "admin")

# Connect to MongoDB with authentication if credentials are provided
if MONGO_USERNAME and MONGO_PASSWORD and ("@" not in MONGO_URI):
    client = MongoClient(
        MONGO_URI,
        username=MONGO_USERNAME,
        password=MONGO_PASSWORD,
        authSource=MONGO_AUTH_SOURCE
    )
else:
    client = MongoClient(MONGO_URI)

# Database and collection setup
db = client["flask_db"]
collection = db["data"]

@app.route("/")
def home():
    return f"Welcome to the Flask app! The current time is: {datetime.now()}"

@app.route("/data", methods=["GET", "POST"])
def handle_data():
    if request.method == "POST":
        data = request.get_json()
        collection.insert_one(data)
        return jsonify({"status": "Data inserted"}), 201
    else:
        # GET
        data = list(collection.find({}, {"_id": 0}))
        return jsonify(data), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
