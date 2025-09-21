from pymongo import MongoClient
import os

# --- CONFIG ---
mongo_uri = os.getenv("MONGO_URI") or "mongodb+srv://<user>:<password>@cluster0.mongodb.net/accessmap?retryWrites=true&w=majority"
client = MongoClient(mongo_uri)
db = client["Pitt_Data"]  # your database
collection = db.Hospitals  # your collection

# --- CHECK SOME DOCUMENTS ---
for doc in collection.find({}, {"Facility": 1, "nearestBusStopDist": 1}).limit(10):
    print(f"{doc.get('Facility')}: {doc.get('nearestBusStopDist')}")
