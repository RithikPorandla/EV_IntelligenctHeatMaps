import pandas as pd
import os
import re

def parse_centroid(wkt_string):
    # Very simple mock centroid extraction from POLYGON string
    # extracts all numbers, takes average of lats and longs
    try:
        nums = [float(x) for x in re.findall(r"[-+]?\d*\.\d+|\d+", wkt_string)]
        # Filter out the '1001' etc if they appear, but wkt usually just coords
        # This is a hacky WKT parser for portfolio demo purposes
        lons = nums[0::2]
        lats = nums[1::2]
        return sum(lats)/len(lats), sum(lons)/len(lons)
    except:
        return 42.26, -71.80

def ingest_parcels():
    raw_path = 'data/raw/worcester_parcels_sample.csv'
    processed_path = 'data/processed/sites.csv'
    
    if not os.path.exists(raw_path):
        print(f"File {raw_path} not found. generating synthetic data...")
        # Fallback if file missing
        df = pd.DataFrame({
            'parcel_id': range(1000, 1010),
            'address': [f'{i} Main St' for i in range(10)],
            'geometry': ['POLYGON((-71.8 42.26))'] * 10
        })
    else:
        print(f"Loading {raw_path}...")
        df = pd.read_csv(raw_path)

    print("Cleaning data...")
    # Clean: remove empty addresses
    df = df.dropna(subset=['address'])
    
    # Feature Engineering: Calculate centroids
    print("Calculating centroids...")
    centroids = df['geometry'].apply(parse_centroid)
    df['lat'] = [c[0] for c in centroids]
    df['lng'] = [c[1] for c in centroids]
    
    # Select columns
    final_df = df[['parcel_id', 'address', 'lat', 'lng']]
    
    os.makedirs(os.path.dirname(processed_path), exist_ok=True)
    final_df.to_csv(processed_path, index=False)
    print(f"Saved {len(final_df)} sites to {processed_path}")

if __name__ == "__main__":
    ingest_parcels()
