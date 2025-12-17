"""
Parcel data ingestion for Worcester, MA.

This script loads candidate EV charging site locations from:
1. REAL DATA: OpenStreetMap buildings (if available)
2. FALLBACK: Grid-based synthetic locations

Data sources:
- OpenStreetMap via Overpass API (free, no authentication)
- Worcester parcel polygons: https://opendata.worcesterma.gov/datasets/parcel-polygons-1/about
- MassGIS parcels: https://www.mass.gov/info-details/massgis-data-property-tax-parcels

Run fetch_real_data.py first to download real data from OSM.
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import numpy as np
import pandas as pd
from pathlib import Path
from app.database import Base
from app.models.site import Site
from app.config import settings


# Worcester bounding box
WORCESTER_BBOX = {
    'lat_min': 42.2084,
    'lat_max': 42.3126,
    'lng_min': -71.8744,
    'lng_max': -71.7277
}

# Path to real data
RAW_DATA_DIR = Path(__file__).parent / "raw"


def generate_grid_points(bbox, grid_size=0.005):
    """
    Generate a regular grid of candidate locations.
    
    Args:
        bbox: Dictionary with lat/lng bounds
        grid_size: Spacing between grid points (degrees)
    
    Returns:
        List of (lat, lng) tuples
    """
    lats = np.arange(bbox['lat_min'], bbox['lat_max'], grid_size)
    lngs = np.arange(bbox['lng_min'], bbox['lng_max'], grid_size)
    
    points = []
    for lat in lats:
        for lng in lngs:
            points.append((lat, lng))
    
    return points


def generate_location_labels(lat, lng):
    """
    Generate a simple location label from coordinates.
    
    In production, would reverse geocode to actual addresses.
    """
    # Simple quadrant-based naming
    center_lat = (WORCESTER_BBOX['lat_min'] + WORCESTER_BBOX['lat_max']) / 2
    center_lng = (WORCESTER_BBOX['lng_min'] + WORCESTER_BBOX['lng_max']) / 2
    
    ns = "North" if lat > center_lat else "South"
    ew = "East" if lng > center_lng else "West"
    
    return f"Worcester {ns}-{ew} (Grid)"


def load_real_buildings():
    """
    Load real building data from OpenStreetMap if available.
    Returns DataFrame or None if not available.
    """
    osm_file = RAW_DATA_DIR / "worcester_buildings_osm.csv"
    
    if not osm_file.exists():
        return None
    
    try:
        df = pd.read_csv(osm_file)
        print(f"  ✓ Loaded {len(df)} real buildings from OpenStreetMap")
        
        # Filter to bounds (in case we got extras)
        df = df[
            (df['lat'] >= WORCESTER_BBOX['lat_min']) &
            (df['lat'] <= WORCESTER_BBOX['lat_max']) &
            (df['lon'] >= WORCESTER_BBOX['lng_min']) &
            (df['lon'] <= WORCESTER_BBOX['lng_max'])
        ]
        
        # Check for parking amenities
        df['is_parking'] = df['amenity'] == 'parking'
        
        print(f"  ✓ {len(df)} buildings within Worcester bounds")
        print(f"  ℹ {df['is_parking'].sum()} parking facilities identified")
        
        return df
        
    except Exception as e:
        print(f"  ⚠ Error loading real buildings: {e}")
        return None


def main():
    """
    Generate candidate sites and store in database.
    Uses real OpenStreetMap data if available, otherwise generates grid.
    """
    print("🗺️  Loading Worcester candidate sites...")
    
    # Create database engine
    engine = create_engine(settings.database_url)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    
    # Clear existing sites for Worcester
    print("Clearing existing Worcester sites...")
    session.query(Site).filter(Site.city == 'worcester').delete()
    session.commit()
    
    # Try to load real building data
    print("Checking for real OpenStreetMap data...")
    buildings_df = load_real_buildings()
    
    sites = []
    
    if buildings_df is not None and len(buildings_df) > 0:
        # Use real building locations
        print(f"Using {len(buildings_df)} real building locations from OSM")
        
        for idx, row in buildings_df.iterrows():
            # Determine if parking lot
            parking_flag = 1 if row.get('is_parking', False) else 0
            
            # Use building name or generate label
            location_label = row.get('name') or generate_location_labels(row['lat'], row['lon'])
            
            site = Site(
                city='worcester',
                lat=row['lat'],
                lng=row['lon'],
                location_label=location_label,
                parcel_id=f"OSM-{int(row['id'])}",
                parking_lot_flag=parking_flag,
                # Initialize other fields with zeros
                traffic_index=0.0,
                pop_density_index=0.0,
                renters_share=0.0,
                income_index=0.0,
                poi_index=0.0,
                municipal_parcel_flag=0,
                score_demand=0.0,
                score_equity=0.0,
                score_traffic=0.0,
                score_grid=0.0,
                score_overall=0.0,
                daily_kwh_estimate=0.0,
            )
            sites.append(site)
        
        print(f"  ✓ Prepared {len(sites)} real building sites")
        print(f"  ✓ {sum(s.parking_lot_flag for s in sites)} identified as parking facilities")
    
    else:
        # Fallback to grid-based approach
        print("⚠️  Real data not available, using grid-based approach")
        print("  ℹ Run 'python fetch_real_data.py' to download OSM data")
        print("Generating grid points...")
        
        points = generate_grid_points(WORCESTER_BBOX, grid_size=0.008)
        print(f"Generated {len(points)} candidate locations")
        
        for idx, (lat, lng) in enumerate(points, start=1):
            location_label = generate_location_labels(lat, lng)
            
            site = Site(
                city='worcester',
                lat=lat,
                lng=lng,
                location_label=location_label,
                parcel_id=f"WORC-GRID-{idx:04d}",
                traffic_index=0.0,
                pop_density_index=0.0,
                renters_share=0.0,
                income_index=0.0,
                poi_index=0.0,
                parking_lot_flag=0,
                municipal_parcel_flag=0,
                score_demand=0.0,
                score_equity=0.0,
                score_traffic=0.0,
                score_grid=0.0,
                score_overall=0.0,
                daily_kwh_estimate=0.0,
            )
            sites.append(site)
    
    # Bulk insert
    print("Inserting sites into database...")
    session.bulk_save_objects(sites)
    session.commit()
    
    print(f"✓ Inserted {len(sites)} sites")
    print("✓ Parcel ingestion complete")
    
    session.close()


if __name__ == "__main__":
    main()
