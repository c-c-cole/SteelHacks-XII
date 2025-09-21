from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})

mongo_uri = os.getenv("MONGO_URI")

client = MongoClient(mongo_uri)


db = client["Pitt_Data"]
collection = db["Hospitals"]


for doc in collection.find().limit(5):
   print(doc)


@app.route("/")
def home():
   return "MongoDB Flask API is running!"




@app.route("/hospitals", methods=["GET"])
def get_hospitals():
   hospitals = collection.find({}, {"_id": 0, "Y": 1, "X": 1, "Facility": 1, "Address": 1})


   result = [[doc["Y"], doc["X"], doc["Facility"], doc["Address"]] for doc in hospitals if "Y" in doc and "X" in doc and "Facility" in doc and "Address" in doc]
   return jsonify(result)