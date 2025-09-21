from pymongo import MongoClient
from geopy.distance import geodesic
import json
import os

# --- CONFIG ---
BUS_STOP_FILE = "./bus_stops.json" 
# SERVICE_TYPE = "hospital"               # filter collection

# --- CONNECT TO MONGO ---
mongo_uri = os.getenv("MONGO_URI") or "mongodb+srv://<user>:<password>@cluster0.mongodb.net/accessmap?retryWrites=true&w=majority"
client = MongoClient(mongo_uri)
db = client["Pitt_Data"]

# --- LOAD BUS STOPS ---
with open(BUS_STOP_FILE, "r") as f:
    bus_data = json.load(f)

bus_stops = []
for rec in bus_data["records"]:
    lat = float(rec[13])   # Latitude column
    lng = float(rec[1])    # Longitude column
    bus_stops.append((lat, lng))

print(f"Loaded {len(bus_stops)} bus stops")

# --- PROCESS HOSPITALS ---
hospitals = db.Hospitals.find()

for h in hospitals:
    print("hi")
    # Use Y/X fields for coordinates
    h_coords = (h["Y"], h["X"])
    min_dist = min(geodesic(h_coords, b).miles for b in bus_stops)

    # Update Mongo with nearest bus distance
    db.Hospitals.update_one(
        {"_id": h["_id"]},
        {"$set": {"nearestBusStopDist": round(min_dist, 3)}}
    )

    print(f"Updated {h['Facility']}: nearest bus stop {min_dist:.3f} miles away")

print("All done!")
