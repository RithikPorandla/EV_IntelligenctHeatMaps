import os
import json
import random

def ingest_parcels():
    """
    Simulates ingesting parcel data from GeoJSON.
    In a real scenario, this would read from data/raw/parcels_worcester.geojson
    and normalize it into a standard format.
    """
    print("Ingesting parcels...")
    # Stub: Just verifying directory exists
    raw_dir = "data/raw"
    processed_dir = "data/processed"
    os.makedirs(raw_dir, exist_ok=True)
    os.makedirs(processed_dir, exist_ok=True)
    
    # In reality:
    # gdf = gpd.read_file(f"{raw_dir}/parcels.geojson")
    # Clean and save to processed
    
    print("Parcel ingestion complete (Stub).")

if __name__ == "__main__":
    ingest_parcels()
