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

# clears all comments on server start
comments_col.delete_many({})  
print("Comments collection cleared on startup.")

def compute_low_high_bus():
    distances = [h['nearestBusStopDist'] for h in db.Hospitals.find() if 'nearestBusStopDist' in h]
    if not distances:
        return 0, 1
    low = np.percentile(distances, 10)
    high = np.percentile(distances, 80)
    return low, high

def compute_low_high_bike():
    distances = [h['nearestBikeDist'] for h in db.Hospitals.find() if 'nearestBikeDist' in h]
    if not distances:
        return 0, 1
    low = np.percentile(distances, 10)
    high = np.percentile(distances, 80)
    return low, high

def compute_income_bounds():
    incomes = [h['median_income'] for h in db.Hospitals.find() if 'median_income' in h]
    if not incomes:
        return 10000, 50000
    low = np.percentile(incomes, 10)
    high = np.percentile(incomes, 90)
    return low, high


@app.route("/service/<service_id>", methods=["GET"])
def get_service(service_id):
    # Fetch hospital
    service = db.Hospitals.find_one({"_id": int(service_id)})
    if not service:
        return jsonify({"error": "Service not found"}), 404

    # --- Accessibility ---
    w_bus = 0.6
    w_bike = 0.3
    w_ada = 0.1  # placeholder for now

    d_bus = service.get('nearestBusStopDist', None)
    d_bike = service.get('nearestBikeDist', None)
    ADA = 1  # placeholder

    bus_low, bus_high = compute_low_high_bus()
    bike_low, bike_high = compute_low_high_bike()

    A_bus = max(0, min(1, 1 - (d_bus - bus_low) / (bus_high - bus_low))) if d_bus is not None else 0
    A_bike = max(0, min(1, 1 - (d_bike - bike_low) / (bike_high - bike_low))) if d_bike is not None else 0

    A = w_bus * A_bus + w_bike * A_bike + w_ada * ADA

    S = 0.8
    M = service.get("median_income", 30000)
    income_low, income_high = compute_income_bounds()

    income_range = income_high - income_low
    if income_range == 0:
        U = 1.25  # midpoint if no variation
    else:
        # clamp M to [income_low, income_high]
        M_clamped = max(income_low, min(M, income_high))
        U = 1.5 - ((M_clamped - income_low) / income_range) * 0.5  # guaranteed 1.0 ≤ U ≤ 1.5

    C = min(1, S * U)


    # --- Gap / Sufficiency ---
    G = 1 - C * (1 - A)

    return jsonify({
        "service_id": service_id,
        "name": service["Facility"],
        "nearestBusStopDist": d_bus,
        "nearestBikeDist": d_bike,
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
