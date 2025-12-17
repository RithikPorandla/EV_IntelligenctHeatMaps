"""
Fetch real open-source datasets for Worcester, MA.

This script downloads publicly available data from various sources:
- OpenStreetMap via Overpass API (no authentication required)
- US Census Bureau (public data)
- OpenStreetMap for POI and parking

All data sources are free and open.
"""
import requests
import json
import pandas as pd
import time
from pathlib import Path

# Create raw data directory
RAW_DIR = Path(__file__).parent / "raw"
RAW_DIR.mkdir(exist_ok=True)

# Worcester bounding box
WORCESTER_BBOX = {
    'south': 42.2084,
    'north': 42.3126,
    'west': -71.8744,
    'east': -71.7277
}


def fetch_osm_buildings():
    """
    Fetch building footprints from OpenStreetMap.
    These will be our candidate sites (building centroids).
    """
    print("📦 Fetching building data from OpenStreetMap...")
    
    # Overpass API query for buildings in Worcester
    overpass_url = "https://overpass-api.de/api/interpreter"
    
    # Query for buildings (commercial, retail, public, parking)
    query = f"""
    [out:json][timeout:60];
    (
      way["building"="commercial"]({WORCESTER_BBOX['south']},{WORCESTER_BBOX['west']},{WORCESTER_BBOX['north']},{WORCESTER_BBOX['east']});
      way["building"="retail"]({WORCESTER_BBOX['south']},{WORCESTER_BBOX['west']},{WORCESTER_BBOX['north']},{WORCESTER_BBOX['east']});
      way["building"="public"]({WORCESTER_BBOX['south']},{WORCESTER_BBOX['west']},{WORCESTER_BBOX['north']},{WORCESTER_BBOX['east']});
      way["amenity"="parking"]({WORCESTER_BBOX['south']},{WORCESTER_BBOX['west']},{WORCESTER_BBOX['north']},{WORCESTER_BBOX['east']});
    );
    out center;
    """
    
    try:
        response = requests.post(overpass_url, data={'data': query}, timeout=90)
        response.raise_for_status()
        data = response.json()
        
        # Extract building centers
        buildings = []
        for element in data.get('elements', []):
            if 'center' in element:
                buildings.append({
                    'id': element['id'],
                    'lat': element['center']['lat'],
                    'lon': element['center']['lon'],
                    'building_type': element.get('tags', {}).get('building', 'unknown'),
                    'amenity': element.get('tags', {}).get('amenity', None),
                    'name': element.get('tags', {}).get('name', None)
                })
        
        df = pd.DataFrame(buildings)
        output_file = RAW_DIR / "worcester_buildings_osm.csv"
        df.to_csv(output_file, index=False)
        
        print(f"  ✓ Fetched {len(buildings)} buildings")
        print(f"  ✓ Saved to {output_file}")
        return df
        
    except Exception as e:
        print(f"  ⚠ Error fetching buildings: {e}")
        print(f"  ℹ Will fall back to grid-based approach")
        return None


def fetch_osm_pois():
    """
    Fetch Points of Interest from OpenStreetMap.
    Used for POI density calculation.
    """
    print("\n🏪 Fetching POI data from OpenStreetMap...")
    
    overpass_url = "https://overpass-api.de/api/interpreter"
    
    # Query for various POI types
    query = f"""
    [out:json][timeout:60];
    (
      node["shop"]({WORCESTER_BBOX['south']},{WORCESTER_BBOX['west']},{WORCESTER_BBOX['north']},{WORCESTER_BBOX['east']});
      node["amenity"~"restaurant|cafe|fast_food|school|hospital|library"]({WORCESTER_BBOX['south']},{WORCESTER_BBOX['west']},{WORCESTER_BBOX['north']},{WORCESTER_BBOX['east']});
      node["office"]({WORCESTER_BBOX['south']},{WORCESTER_BBOX['west']},{WORCESTER_BBOX['north']},{WORCESTER_BBOX['east']});
    );
    out;
    """
    
    try:
        response = requests.post(overpass_url, data={'data': query}, timeout=90)
        response.raise_for_status()
        data = response.json()
        
        # Extract POIs
        pois = []
        for element in data.get('elements', []):
            if element['type'] == 'node':
                pois.append({
                    'id': element['id'],
                    'lat': element['lat'],
                    'lon': element['lon'],
                    'type': element.get('tags', {}).get('shop') or 
                           element.get('tags', {}).get('amenity') or
                           element.get('tags', {}).get('office', 'unknown'),
                    'name': element.get('tags', {}).get('name', None)
                })
        
        df = pd.DataFrame(pois)
        output_file = RAW_DIR / "worcester_pois_osm.csv"
        df.to_csv(output_file, index=False)
        
        print(f"  ✓ Fetched {len(pois)} POIs")
        print(f"  ✓ Saved to {output_file}")
        return df
        
    except Exception as e:
        print(f"  ⚠ Error fetching POIs: {e}")
        return None


def fetch_osm_roads():
    """
    Fetch road network from OpenStreetMap.
    Used for traffic estimation based on road classification.
    """
    print("\n🛣️  Fetching road network from OpenStreetMap...")
    
    overpass_url = "https://overpass-api.de/api/interpreter"
    
    # Query for major roads
    query = f"""
    [out:json][timeout:60];
    (
      way["highway"~"motorway|trunk|primary|secondary"]({WORCESTER_BBOX['south']},{WORCESTER_BBOX['west']},{WORCESTER_BBOX['north']},{WORCESTER_BBOX['east']});
    );
    out geom;
    """
    
    try:
        response = requests.post(overpass_url, data={'data': query}, timeout=90)
        response.raise_for_status()
        data = response.json()
        
        # Extract roads with their classifications
        roads = []
        for element in data.get('elements', []):
            if element['type'] == 'way' and 'geometry' in element:
                road_type = element.get('tags', {}).get('highway', 'unknown')
                name = element.get('tags', {}).get('name', None)
                
                # Get road segments
                for point in element['geometry']:
                    roads.append({
                        'way_id': element['id'],
                        'lat': point['lat'],
                        'lon': point['lon'],
                        'highway_type': road_type,
                        'name': name
                    })
        
        df = pd.DataFrame(roads)
        output_file = RAW_DIR / "worcester_roads_osm.csv"
        df.to_csv(output_file, index=False)
        
        print(f"  ✓ Fetched {len(roads)} road segments")
        print(f"  ✓ Saved to {output_file}")
        return df
        
    except Exception as e:
        print(f"  ⚠ Error fetching roads: {e}")
        return None


def fetch_census_data():
    """
    Fetch Census data for Worcester County, MA.
    Using the public Census API (no key required for basic queries).
    """
    print("\n👥 Fetching demographic data from US Census Bureau...")
    
    # Worcester County FIPS: 25027 (MA = 25, Worcester County = 027)
    # Using 2021 5-year ACS estimates (most recent stable data)
    
    try:
        # Query for census tract data
        # Variables:
        # B01003_001E: Total population
        # B19013_001E: Median household income
        # B25003_003E: Renter-occupied housing units
        # B25003_001E: Total occupied housing units
        
        census_url = "https://api.census.gov/data/2021/acs/acs5"
        
        params = {
            'get': 'B01003_001E,B19013_001E,B25003_003E,B25003_001E,NAME',
            'for': 'tract:*',
            'in': 'state:25 county:027'  # Massachusetts, Worcester County
        }
        
        response = requests.get(census_url, params=params, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        
        # Convert to DataFrame
        headers = data[0]
        rows = data[1:]
        df = pd.DataFrame(rows, columns=headers)
        
        # Rename columns for clarity
        df = df.rename(columns={
            'B01003_001E': 'total_population',
            'B19013_001E': 'median_household_income',
            'B25003_003E': 'renter_occupied',
            'B25003_001E': 'total_occupied',
            'NAME': 'tract_name'
        })
        
        # Calculate renter share
        df['renter_occupied'] = pd.to_numeric(df['renter_occupied'], errors='coerce')
        df['total_occupied'] = pd.to_numeric(df['total_occupied'], errors='coerce')
        df['renters_share'] = df['renter_occupied'] / df['total_occupied']
        
        # Convert numeric columns
        df['total_population'] = pd.to_numeric(df['total_population'], errors='coerce')
        df['median_household_income'] = pd.to_numeric(df['median_household_income'], errors='coerce')
        
        output_file = RAW_DIR / "worcester_census_tracts.csv"
        df.to_csv(output_file, index=False)
        
        print(f"  ✓ Fetched data for {len(df)} census tracts")
        print(f"  ✓ Saved to {output_file}")
        return df
        
    except Exception as e:
        print(f"  ⚠ Error fetching Census data: {e}")
        print(f"  ℹ Note: Census API can be slow or temporarily unavailable")
        return None


def fetch_census_tract_boundaries():
    """
    Fetch census tract boundary coordinates.
    Using Census TIGER/Line shapefiles via their API.
    """
    print("\n🗺️  Fetching census tract boundaries...")
    
    try:
        # Worcester County census tracts from TIGER/Line
        # Using a simplified version for faster download
        url = "https://www2.census.gov/geo/tiger/TIGER2021/TRACT/tl_2021_25_tract.zip"
        
        print(f"  ℹ Downloading tract boundaries (this may take a moment)...")
        response = requests.get(url, timeout=120, stream=True)
        response.raise_for_status()
        
        zip_file = RAW_DIR / "census_tracts.zip"
        with open(zip_file, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        print(f"  ✓ Downloaded tract boundaries")
        print(f"  ✓ Saved to {zip_file}")
        print(f"  ℹ Note: Extract this file and filter for Worcester County (COUNTYFP=027)")
        
        return True
        
    except Exception as e:
        print(f"  ⚠ Error fetching tract boundaries: {e}")
        print(f"  ℹ Boundaries are optional - can use tract centers instead")
        return None


def main():
    """
    Run all data fetching operations.
    """
    print("=" * 60)
    print("MA EV ChargeMap - Real Data Fetcher")
    print("=" * 60)
    print("\nFetching open-source datasets from:")
    print("  - OpenStreetMap (buildings, POIs, roads)")
    print("  - US Census Bureau (demographics)")
    print("\nThis may take a few minutes...\n")
    
    results = {}
    
    # Fetch OSM data (building locations for candidate sites)
    results['buildings'] = fetch_osm_buildings()
    time.sleep(2)  # Be nice to Overpass API
    
    # Fetch POIs
    results['pois'] = fetch_osm_pois()
    time.sleep(2)
    
    # Fetch roads
    results['roads'] = fetch_osm_roads()
    time.sleep(2)
    
    # Fetch Census data
    results['census'] = fetch_census_data()
    
    # Optionally fetch tract boundaries
    results['boundaries'] = fetch_census_tract_boundaries()
    
    print("\n" + "=" * 60)
    print("Data Fetching Complete!")
    print("=" * 60)
    
    print("\n📊 Summary:")
    if results['buildings'] is not None:
        print(f"  ✓ Buildings: {len(results['buildings'])} locations")
    else:
        print(f"  ⚠ Buildings: Failed (will use grid)")
    
    if results['pois'] is not None:
        print(f"  ✓ POIs: {len(results['pois'])} points")
    else:
        print(f"  ⚠ POIs: Failed (will use synthetic)")
    
    if results['roads'] is not None:
        print(f"  ✓ Roads: {len(results['roads'])} segments")
    else:
        print(f"  ⚠ Roads: Failed (will use synthetic)")
    
    if results['census'] is not None:
        print(f"  ✓ Census: {len(results['census'])} tracts")
    else:
        print(f"  ⚠ Census: Failed (will use synthetic)")
    
    print(f"\n📁 All data saved to: {RAW_DIR}")
    print("\nNext steps:")
    print("  1. Run the data pipeline: cd ../data && ./run_pipeline.sh")
    print("  2. The pipeline will automatically use real data if available")
    print("  3. Falls back to synthetic data if downloads failed")
    
    return results


if __name__ == "__main__":
    main()
