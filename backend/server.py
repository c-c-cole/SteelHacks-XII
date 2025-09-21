from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient
from dotenv import load_dotenv
import os
import numpy as np

load_dotenv()
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})

mongo_uri = os.getenv("MONGO_URI")

client = MongoClient(mongo_uri)
db = client["Pitt_Data"]
collection = db["Hospitals"]

# precompute low/high for A rating
distances = [h['nearestBusStopDist'] for h in db.Hospitals.find()]
low = np.percentile(distances, 10)
high = np.percentile(distances, 90)

@app.route("/service/<service_id>", methods=["GET"])
def get_service(service_id):
    service = db.Hospitals.find_one({"_id": int(service_id)}) # adapt type to what the _id will be
    if not service:
        return jsonify({"error": "Service not found"}), 404

    # compute A
    d = service['nearestBusStopDist']
    A = max(0, min(1, 1 - (d - low)/(high - low)))

    # compute criticality C 
    S = 0.8 # hospital importance (static now)
    U = 1 # placeholder for neighborhood adjustment
    C = min(1, S * U)

    G = C * (1 - A) # Critical Access Gap

    return jsonify({
        "service_id": service_id,
        "name": service["Facility"],
        "nearestBusStopDist": d,
        "A": round(A, 3),
        "C": C,
        "G": round(G, 3)
    })


@app.route("/")
def home():
   return "MongoDB Flask API is running!"


@app.route("/hospitals", methods=["GET"])
def get_hospitals():
   hospitals = collection.find({}, {"_id": 0, "Y": 1, "X": 1, "Facility": 1, "Address": 1})


   result = [[doc["Y"], doc["X"], doc["Facility"], doc["Address"]] for doc in hospitals if "Y" in doc and "X" in doc and "Facility" in doc and "Address" in doc]
   return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)
