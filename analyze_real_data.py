#!/usr/bin/env python3
"""
Analyze the real data we downloaded
"""
import pandas as pd
import numpy as np

print("\n" + "=" * 70)
print("REAL DATA ANALYSIS - MA EV ChargeMap")
print("=" * 70 + "\n")

# Load all datasets
buildings = pd.read_csv('data/raw/worcester_buildings_osm.csv')
pois = pd.read_csv('data/raw/worcester_pois_osm.csv')
census = pd.read_csv('data/raw/worcester_census_tracts.csv')

print("📊 DATASET SIZES")
print("-" * 70)
print(f"  Buildings (OpenStreetMap):  {len(buildings):,} real locations")
print(f"  POIs (OpenStreetMap):       {len(pois):,} real points")
print(f"  Census Tracts:              {len(census):,} tracts")
print()

print("🏢 BUILDING ANALYSIS")
print("-" * 70)
print(f"  Total buildings: {len(buildings)}")
print(f"  Parking facilities: {(buildings['amenity'] == 'parking').sum()}")
print(f"  Named buildings: {buildings['name'].notna().sum()}")
print()

# Geographic bounds
print("  Geographic Coverage:")
print(f"    Latitude:  {buildings['lat'].min():.4f} to {buildings['lat'].max():.4f}")
print(f"    Longitude: {buildings['lon'].min():.4f} to {buildings['lon'].max():.4f}")
print()

print("🏪 POI ANALYSIS")
print("-" * 70)
top_poi_types = pois['type'].value_counts().head(10)
for poi_type, count in top_poi_types.items():
    print(f"  {poi_type:20} {count:3} locations")
print()

print("👥 CENSUS ANALYSIS")
print("-" * 70)
# Clean census data
census_clean = census[census['total_population'].notna()]
census_clean = census_clean[census_clean['median_household_income'] > 0]

if len(census_clean) > 0:
    print(f"  Valid census tracts: {len(census_clean)}")
    print(f"  Total population: {census_clean['total_population'].sum():,.0f}")
    print(f"  Avg tract population: {census_clean['total_population'].mean():.0f}")
    print(f"  Median household income: ${census_clean['median_household_income'].median():,.0f}")
    print(f"  Avg renter share: {census_clean['renters_share'].mean():.1%}")
else:
    print("  (Census data needs cleaning)")
print()

print("🗺️  SPATIAL DISTRIBUTION")
print("-" * 70)

# Divide into quadrants
center_lat = buildings['lat'].median()
center_lon = buildings['lon'].median()

buildings['quadrant'] = 'Other'
buildings.loc[(buildings['lat'] >= center_lat) & (buildings['lon'] >= center_lon), 'quadrant'] = 'NE'
buildings.loc[(buildings['lat'] >= center_lat) & (buildings['lon'] < center_lon), 'quadrant'] = 'NW'
buildings.loc[(buildings['lat'] < center_lat) & (buildings['lon'] >= center_lon), 'quadrant'] = 'SE'
buildings.loc[(buildings['lat'] < center_lat) & (buildings['lon'] < center_lon), 'quadrant'] = 'SW'

print("  Buildings by quadrant:")
for quad, count in buildings['quadrant'].value_counts().items():
    print(f"    {quad}: {count:4} buildings")
print()

pois['quadrant'] = 'Other'
pois.loc[(pois['lat'] >= center_lat) & (pois['lon'] >= center_lon), 'quadrant'] = 'NE'
pois.loc[(pois['lat'] >= center_lat) & (pois['lon'] < center_lon), 'quadrant'] = 'NW'
pois.loc[(pois['lat'] < center_lat) & (pois['lon'] >= center_lon), 'quadrant'] = 'SE'
pois.loc[(pois['lat'] < center_lat) & (pois['lon'] < center_lon), 'quadrant'] = 'SW'

print("  POIs by quadrant:")
for quad, count in pois['quadrant'].value_counts().items():
    print(f"    {quad}: {count:4} POIs")
print()

print("💡 KEY INSIGHTS")
print("-" * 70)
print(f"  1. We have {len(buildings):,} REAL building locations from OpenStreetMap")
print(f"     - Not a synthetic grid! These are actual Worcester buildings.")
print(f"     - {(buildings['amenity'] == 'parking').sum()} already identified as parking")
print()
print(f"  2. We have {len(pois):,} REAL points of interest")
print(f"     - Top category: {top_poi_types.index[0]} ({top_poi_types.values[0]} locations)")
print(f"     - Can compute actual POI density, not estimates")
print()
print(f"  3. We have REAL census demographics")
print(f"     - Actual income and renter data from Census Bureau")
print(f"     - Can join spatially to candidate sites")
print()
print("  4. Data is VERIFIABLE")
print("     - Anyone can check these buildings on openstreetmap.org")
print("     - Census data is from official census.gov API")
print()

print("🎯 PORTFOLIO VALUE")
print("-" * 70)
print("  Instead of saying:")
print("    'I built a tool with synthetic data'")
print()
print("  You can now say:")
print("    'I integrated OpenStreetMap and US Census Bureau APIs")
print("     to process 1,445 real buildings and 548 POIs with")
print("     191 census tracts of demographic data'")
print()

print("=" * 70)
print("✅ Real data successfully downloaded and analyzed!")
print("=" * 70)
print()
print("Next: Run the full pipeline with './data/run_pipeline.sh'")
print("      to process all this data into scored EV charging sites!")
print()
