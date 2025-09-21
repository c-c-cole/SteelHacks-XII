from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient
from dotenv import load_dotenv
import os
import numpy as np
from bson.objectid import ObjectId


load_dotenv()
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})

mongo_uri = os.getenv("MONGO_URI")

client = MongoClient(mongo_uri)
db = client["Pitt_Data"]
collection = db["Hospitals"]

comments_col = db["Comments"]

def compute_low_high():
    distances = [h['nearestBusStopDist'] for h in db.Hospitals.find() if 'nearestBusStopDist' in h]
    if not distances: # avoid crash if collection is empty
        return 0, 1  
    low = np.percentile(distances, 10)
    high = np.percentile(distances, 90)
    return low, high


@app.route("/service/<service_id>", methods=["GET"])
def get_service(service_id):
    low, high = compute_low_high()

    service = db.Hospitals.find_one({"_id": int(service_id)})
    if not service:
        return jsonify({"error": "Service not found"}), 404

    d = service.get('nearestBusStopDist', None)
    if d is None:
        return jsonify({"error": "Bus distance not found for this service"}), 400
    A = max(0, min(1, 1 - (d - low) / (high - low)))

    S = 0.8
    M = service.get("median_income", 30000)
    income_low = 10000
    income_high = 50000
    U = 1.5 - ((M - income_low) / (income_high - income_low)) * 0.5
    U = max(0, min(1, U))

    C = min(1, S * U)
    G = 1 - C * (1 - A)

    return jsonify({
        "service_id": service_id,
        "name": service["Facility"],
        "nearestBusStopDist": d,
        "median_income": M,
        "A": round(A, 3),
        "C": round(C, 3),
        "G": round(G, 3)
    })


@app.route("/")
def home():
   return "MongoDB Flask API is running!"


@app.route("/hospitals", methods=["GET"])
def get_hospitals():
   hospitals = collection.find({}, {"_id": 1, "Y": 1, "X": 1, "Facility": 1, "Address": 1})


   result = [[doc["_id"], doc["Y"], doc["X"], doc["Facility"], doc["Address"]] for doc in hospitals if "_id" in doc and "Y" in doc and "X" in doc and "Facility" in doc and "Address" in doc]
   return jsonify(result)



@app.route("/comments/<int:hospital_id>", methods=["GET", "POST"])
def comments(hospital_id):
    if request.method == "GET":
        # fetch all comments for this hospital
        hospital_comments = list(comments_col.find({"hospital_id": hospital_id}, {"_id": 0}))
        return jsonify(hospital_comments)

    elif request.method == "POST":
        data = request.json
        if not data or "user" not in data or "text" not in data:
            return jsonify({"error": "Invalid comment data"}), 400

        comment_doc = {
            "hospital_id": hospital_id,
            "user": data["user"],
            "text": data["text"]
        }
        comments_col.insert_one(comment_doc)
        return jsonify(comment_doc), 201

if __name__ == "__main__":
    app.run(debug=True)
