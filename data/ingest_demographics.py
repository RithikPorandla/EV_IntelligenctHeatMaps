"""
Demographics data ingestion for Worcester, MA.

This script generates synthetic demographic features for each candidate site.
In production, would load from MAPC DataCommon or Census data.

Data sources (for reference):
- MAPC DataCommon: https://datacommon.mapc.org/
- Community data: https://datacommon.mapc.org/communities
- Census API: https://www.census.gov/data/developers/data-sets.html

Features generated:
- Population density index (0-1)
- Median income index (0-1)
- Renter share (0-1)
- Points of interest index (0-1)
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


# Worcester center (downtown has higher density/activity)
WORCESTER_CENTER = {'lat': 42.2626, 'lng': -71.8023}


def distance_to_center(lat, lng):
    """Calculate approximate distance to city center."""
    dlat = lat - WORCESTER_CENTER['lat']
    dlng = lng - WORCESTER_CENTER['lng']
    return np.sqrt(dlat**2 + dlng**2)


def generate_pop_density_index(lat, lng, seed=42):
    """
    Generate population density index.
    
    Higher near city center, with some randomness.
    """
    np.random.seed(seed + int(lat * 1000))
    dist = distance_to_center(lat, lng)
    
    # Density decreases with distance from center
    base_density = max(0, 1.0 - dist * 10)
    
    # Add noise
    noise = np.random.uniform(-0.2, 0.2)
    density = np.clip(base_density + noise, 0, 1)
    
    return density


def generate_income_index(lat, lng, seed=42):
    """
    Generate income index (0 = low income, 1 = high income).
    
    Varies by neighborhood with some spatial correlation.
    """
    np.random.seed(seed + int(lat * 1000) + int(lng * 1000))
    
    # Income tends to be higher on the west side
    west_bias = (lng - WORCESTER_CENTER['lng']) * 5
    
    base_income = 0.5 + west_bias
    noise = np.random.uniform(-0.25, 0.25)
    income = np.clip(base_income + noise, 0, 1)
    
    return income


def generate_renters_share(pop_density, income_index, seed=42):
    """
    Generate renters share.
    
    Higher in denser areas and lower-income neighborhoods.
    """
    np.random.seed(seed)
    
    # More renters in dense, lower-income areas
    base_renters = 0.3 + 0.4 * pop_density + 0.2 * (1 - income_index)
    noise = np.random.uniform(-0.15, 0.15)
    renters = np.clip(base_renters + noise, 0, 1)
    
    return renters


def generate_poi_index(lat, lng, pop_density, seed=42):
    """
    Generate points of interest (jobs, retail, schools) index.
    
    Correlated with population density and proximity to center.
    """
    np.random.seed(seed + int(lat * 1000))
    dist = distance_to_center(lat, lng)
    
    # POI higher near center and in dense areas
    base_poi = 0.5 * (1 - dist * 8) + 0.5 * pop_density
    noise = np.random.uniform(-0.2, 0.2)
    poi = np.clip(base_poi + noise, 0, 1)
    
    return poi


def generate_parking_lot_flag(poi_index, seed=42):
    """
    Generate parking lot flag (higher probability in commercial areas).
    """
    np.random.seed(seed)
    # 30% base probability, higher in high-POI areas
    prob = 0.3 + 0.3 * poi_index
    return 1 if np.random.random() < prob else 0


def generate_municipal_flag(lat, lng, seed=42):
    """
    Generate municipal parcel flag (random, ~10% of sites).
    """
    np.random.seed(seed + int(lat * 1000) + int(lng * 1000))
    return 1 if np.random.random() < 0.1 else 0


def main():
    """
    Generate demographic features for all sites.
    """
    print("👥 Generating demographic features for Worcester sites...")
    
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
    
    # Generate features for each site
    for idx, site in enumerate(sites):
        # Use site ID as seed for reproducibility
        seed = site.id
        
        # Generate demographic features
        pop_density = generate_pop_density_index(site.lat, site.lng, seed)
        income = generate_income_index(site.lat, site.lng, seed)
        renters = generate_renters_share(pop_density, income, seed)
        poi = generate_poi_index(site.lat, site.lng, pop_density, seed)
        parking = generate_parking_lot_flag(poi, seed)
        municipal = generate_municipal_flag(site.lat, site.lng, seed)
        
        # Update site
        site.pop_density_index = round(pop_density, 3)
        site.income_index = round(income, 3)
        site.renters_share = round(renters, 3)
        site.poi_index = round(poi, 3)
        site.parking_lot_flag = parking
        site.municipal_parcel_flag = municipal
        
        if (idx + 1) % 100 == 0:
            print(f"  Processed {idx + 1}/{len(sites)} sites")
    
    # Commit changes
    print("Saving to database...")
    session.commit()
    
    print(f"✓ Updated {len(sites)} sites with demographic features")
    print("✓ Demographics ingestion complete")
    
    session.close()


if __name__ == "__main__":
    main()
