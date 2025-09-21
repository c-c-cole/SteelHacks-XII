from pymongo import MongoClient
from geopy.distance import geodesic
import csv
import os

# --- CONFIG ---
BIKE_STATION_FILE = "./bikes.csv"

# --- CONNECT TO MONGO ---
mongo_uri = os.getenv("MONGO_URI")
client = MongoClient(mongo_uri)
db = client["Pitt_Data"]

# --- LOAD BIKE STATIONS ---
bike_stations = []
with open(BIKE_STATION_FILE, newline='') as f:
    reader = csv.DictReader(f)
    for row in reader:
        lat = float(row["Latitude"])
        lng = float(row["Longitude"])
        bike_stations.append((lat, lng))

print(f"Loaded {len(bike_stations)} bike stations")

# --- PROCESS HOSPITALS ---
hospitals = db.Hospitals.find()

for h in hospitals:
    h_coords = (h["Y"], h["X"])  # Use your existing Y/X fields
    # Find nearest bike station distance
    min_dist = min(geodesic(h_coords, b).miles for b in bike_stations)

    # Update MongoDB with nearest bike distance
    db.Hospitals.update_one(
        {"_id": h["_id"]},
        {"$set": {"nearestBikeDist": round(min_dist, 3)}}
    )

    print(f"Updated {h['Facility']}: nearest bike station {min_dist:.3f} miles away")

print("All done!")
