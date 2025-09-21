import json
import pandas as pd
from pymongo import MongoClient
from shapely.geometry import shape, Point
import geopandas as gpd
import os

# --- CONFIG ---
NEIGHBORHOOD_CSV = "./neighborhoods.csv"
NEIGHBORHOOD_GEOJSON = "./neighborhoods.geojson"

# --- CONNECT TO MONGO ---
mongo_uri = os.getenv("MONGO_URI")
print("Mongo URI:", mongo_uri)
client = MongoClient(mongo_uri)
db = client["Pitt_Data"]

# --- LOAD NEIGHBORHOOD CSV ---
print("Loading neighborhood CSV...")
neighborhoods_df = pd.read_csv(NEIGHBORHOOD_CSV)
# normalize neighborhood names
neighborhoods_df["hood_norm"] = neighborhoods_df["Neighborhood_2010_HOOD"].str.strip().str.lower()
hood_to_income = dict(zip(neighborhoods_df["hood_norm"],
                          neighborhoods_df["SNAP_All_csv_2009_Median_Income"]))

# --- LOAD NEIGHBORHOOD GEOJSON ---
print("Loading neighborhood GeoJSON...")
gdf = gpd.read_file(NEIGHBORHOOD_GEOJSON)

# Convert GeoJSON to WGS84 lat/lon if it's projected
if gdf.crs is not None and gdf.crs.to_epsg() != 4326:
    print(f"Converting neighborhoods GeoJSON from {gdf.crs} to EPSG:4326...")
    gdf = gdf.to_crs(epsg=4326)

# normalize GeoJSON neighborhood names
gdf["hood_norm"] = gdf["Neighborhood_2010_HOOD"].str.strip().str.lower()

# --- ASSIGN MEDIAN INCOME TO HOSPITALS ---
hospitals = list(db.Hospitals.find())
print(f"Processing {len(hospitals)} hospitals...")

for h in hospitals:
    h_point = Point(h["X"], h["Y"])  # X=lon, Y=lat
    median_income = None

    for _, feature in gdf.iterrows():
        polygon = feature["geometry"]
        if polygon.contains(h_point):
            hood_name = feature["hood_norm"]
            median_income = hood_to_income.get(hood_name)
            break

    if median_income is None:
        print(f"WARNING: Could not find median income for {h['Facility']}. Using default 30000.")
        median_income = 30000  # fallback default

    db.Hospitals.update_one(
        {"_id": h["_id"]},
        {"$set": {"median_income": median_income}}
    )

    print(f"{h['Facility']} -> median_income: {median_income}")

print("All hospitals updated with neighborhood median income!")
