"""
Traffic data ingestion for Worcester, MA.

This script generates synthetic traffic indexes for each candidate site.
In production, would load from MassDOT traffic count data.

Data sources (for reference):
- MassDOT Traffic Inventory: https://geo-massdot.opendata.arcgis.com/datasets/traffic-inventory-2023
- Road data: https://geo-massdot.opendata.arcgis.com

The traffic index represents normalized traffic volume/activity near each site.
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import numpy as np
from app.database import Base
from app.models.site import Site
from app.config import settings


# Worcester center and major corridors
WORCESTER_CENTER = {'lat': 42.2626, 'lng': -71.8023}

# Major road corridors (simplified)
MAJOR_CORRIDORS = [
    {'name': 'I-290', 'lat': 42.255, 'lng': -71.810, 'influence': 0.02},
    {'name': 'Route 9', 'lat': 42.278, 'lng': -71.800, 'influence': 0.015},
    {'name': 'Main St', 'lat': 42.263, 'lng': -71.800, 'influence': 0.01},
]


def distance_to_point(lat1, lng1, lat2, lng2):
    """Calculate approximate distance between two points."""
    return np.sqrt((lat1 - lat2)**2 + (lng1 - lng2)**2)


def generate_traffic_index(lat, lng, seed=42):
    """
    Generate traffic index based on proximity to corridors and downtown.
    
    Traffic is highest:
    - Near major road corridors
    - Near downtown center
    - With some randomness
    """
    np.random.seed(seed + int(lat * 1000))
    
    # Base traffic from downtown proximity
    dist_to_center = distance_to_point(lat, lng, WORCESTER_CENTER['lat'], WORCESTER_CENTER['lng'])
    center_traffic = max(0, 1.0 - dist_to_center * 8)
    
    # Traffic from major corridors
    corridor_traffic = 0
    for corridor in MAJOR_CORRIDORS:
        dist = distance_to_point(lat, lng, corridor['lat'], corridor['lng'])
        corridor_traffic += max(0, 1.0 - dist / corridor['influence'])
    
    corridor_traffic = min(corridor_traffic, 1.0)
    
    # Combine (corridors weighted more heavily)
    base_traffic = 0.3 * center_traffic + 0.7 * corridor_traffic
    
    # Add noise
    noise = np.random.uniform(-0.15, 0.15)
    traffic = np.clip(base_traffic + noise, 0, 1)
    
    return traffic


def main():
    """
    Generate traffic features for all sites.
    """
    print("🚗 Generating traffic features for Worcester sites...")
    
    # Connect to database
    engine = create_engine(settings.database_url)
    Session = sessionmaker(bind=engine)
    session = Session()
    
    # Get all Worcester sites
    sites = session.query(Site).filter(Site.city == 'worcester').all()
    print(f"Processing {len(sites)} sites...")
    
    if len(sites) == 0:
        print("⚠️  No sites found. Run ingest_parcels.py first.")
        return
    
    # Generate traffic index for each site
    for idx, site in enumerate(sites):
        # Use site ID as seed for reproducibility
        seed = site.id
        
        # Generate traffic index
        traffic = generate_traffic_index(site.lat, site.lng, seed)
        
        # Update site
        site.traffic_index = round(traffic, 3)
        
        if (idx + 1) % 100 == 0:
            print(f"  Processed {idx + 1}/{len(sites)} sites")
    
    # Commit changes
    print("Saving to database...")
    session.commit()
    
    print(f"✓ Updated {len(sites)} sites with traffic features")
    print("✓ Traffic ingestion complete")
    
    session.close()


if __name__ == "__main__":
    main()
