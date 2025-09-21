from pymongo import MongoClient
import os

# --- Connect to MongoDB ---
mongo_uri = os.getenv("MONGO_URI") 
client = MongoClient(mongo_uri)
db = client["Pitt_Data"]
hospitals = db["Hospitals"]

# --- Mock records ---
mock_records = [
    {
        "_id": 24,
        "Facility": "Friendship Parklet",
        "Address": "123 Rich St, Pittsburgh, PA 15213",
        "Y": 40.46254,
        "X": -79.94587,
        "nearestBusStopDist": 0.5,
        "nearestBikeDist": 1,
        "median_income": 20000
    },
    {
        "_id": 25,
        "Facility": "Schenley Park",
        "Address": "Schenley Drive and Panther Hollow Road",
        "Y": 40.4344,
        "X": -79.9428,
        "nearestBusStopDist": 0.1,
        "nearestBikeDist": 0.1,
        "median_income": 48000
    }
]

# --- Insert into collection ---
for record in mock_records:
    # Use replace_one with upsert=True to avoid duplicates if running multiple times
    hospitals.replace_one({"_id": record["_id"]}, record, upsert=True)

print("Inserted/updated mock records successfully!")
