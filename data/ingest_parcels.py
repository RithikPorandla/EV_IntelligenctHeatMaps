"""
Parcel data ingestion for Worcester, MA.

This script generates candidate EV charging site locations based on a grid
over Worcester. In a production system, this would load actual parcel data
from MassGIS or Worcester open data portal.

Data source (for reference):
- Worcester parcel polygons: https://opendata.worcesterma.gov/datasets/parcel-polygons-1/about
- MassGIS parcels: https://www.mass.gov/info-details/massgis-data-property-tax-parcels

For this portfolio project, we create a synthetic grid of candidate locations.
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import numpy as np
import pandas as pd
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


def main():
    """
    Generate candidate sites and store in database.
    """
    print("🗺️  Generating Worcester candidate sites...")
    
    # Create database engine
    engine = create_engine(settings.database_url)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    
    # Clear existing sites for Worcester
    print("Clearing existing Worcester sites...")
    session.query(Site).filter(Site.city == 'worcester').delete()
    session.commit()
    
    # Generate grid points
    print("Generating grid points...")
    points = generate_grid_points(WORCESTER_BBOX, grid_size=0.008)
    print(f"Generated {len(points)} candidate locations")
    
    # Create site records (without scores yet)
    sites = []
    for idx, (lat, lng) in enumerate(points, start=1):
        location_label = generate_location_labels(lat, lng)
        
        site = Site(
            city='worcester',
            lat=lat,
            lng=lng,
            location_label=location_label,
            parcel_id=f"WORC-GRID-{idx:04d}",
            # Initialize with zeros - will be computed later
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
