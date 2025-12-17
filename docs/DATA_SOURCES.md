# Data Sources

This document describes the data sources used (or referenced) in the MA EV ChargeMap project.

## Overview

For this **portfolio project**, data is primarily **synthetic/simulated** to demonstrate the data pipeline, analysis, and ML capabilities without requiring extensive manual data downloads or API keys.

However, the project is structured to integrate with real Massachusetts open data sources, which are documented below for reference.

---

## Data Philosophy

### Portfolio vs. Production

**Portfolio Version (Current)**
- Uses synthetic data generation to simulate realistic patterns
- Allows complete project demonstration without data access barriers
- Focuses on showcasing data engineering and analysis skills
- All pipeline code is real and reusable

**Production Version (Future)**
- Would integrate actual MA open data sources
- Automated data ingestion via APIs where available
- Manual download steps documented for datasets without APIs
- Data validation and quality checks

---

## 1. Massachusetts State Data Portals

### Mass.gov Open Data
- **URL**: https://data.mass.gov
- **Relevance**: Central hub for state government datasets
- **Topics Used**:
  - Energy & Environment: https://data.mass.gov/browse/energy-and-environment
  - Housing & Development
  - Transportation

### MassGIS (Massachusetts Geographic Information System)
- **URL**: https://www.mass.gov/orgs/massgis-bureau-of-geographic-information
- **Data Portal**: https://gis.data.mass.gov/
- **Relevance**: Authoritative source for MA geospatial data

**Key Datasets:**
- **Property Tax Parcels**: https://www.mass.gov/info-details/massgis-data-property-tax-parcels
  - Use: Candidate site locations (parcel centroids)
  - Format: Shapefile/GeoJSON
  - Coverage: Statewide, town-by-town

### Environmental Justice & Energy Data
- **MA Clean Energy & Climate Metrics**: https://www.mass.gov/info-details/massachusetts-clean-energy-and-climate-metrics
  - Use: Policy context, target setting
  
- **Environmental Data**: https://www.mass.gov/info-details/environmental-data-and-information
  - Use: Environmental justice area designations

---

## 2. Worcester-Specific Data

### Worcester Open Data Portal
- **URL**: https://opendata.worcesterma.gov
- **Parcel Polygons**: https://opendata.worcesterma.gov/datasets/parcel-polygons-1/about
  - Use: City parcel boundaries and identifiers
  - Format: GeoJSON, Shapefile, CSV
  - Update Frequency: Periodic

**How We Use It:**
1. Download Worcester parcel polygons
2. Filter for candidate site types (commercial, municipal, parking)
3. Compute centroids as candidate EV charging locations
4. Store in database with parcel IDs for reference

---

## 3. Demographics & Equity Data

### MAPC DataCommon
- **URL**: https://datacommon.mapc.org
- **Community Data**: https://datacommon.mapc.org/communities
- **Relevance**: Regional demographic and economic data

**Key Metrics:**
- Population density (by census tract/block group)
- Median household income
- Renter vs. owner-occupied housing
- Vehicle availability
- Educational attainment
- Employment centers

**Integration Approach:**
1. Export demographic data by census geography
2. Spatial join to candidate sites
3. Normalize to 0-1 indexes for scoring

### US Census Bureau
- **Census API**: https://www.census.gov/data/developers/data-sets.html
- **American Community Survey (ACS)**
  - 5-year estimates for stable demographics
  - Detailed tables on housing, income, transportation

**Relevant Tables:**
- **B25003**: Tenure (owner vs. renter)
- **B19013**: Median household income
- **B08201**: Household vehicle availability
- **B01003**: Total population

---

## 4. Traffic & Transportation Data

### MassDOT Open Data
- **Portal**: https://geo-massdot.opendata.arcgis.com
- **Traffic Inventory**: https://geo-massdot.opendata.arcgis.com/datasets/traffic-inventory-2023
  - Use: Annual Average Daily Traffic (AADT) counts
  - Format: GeoJSON, CSV
  - Coverage: State highways and major roads

**How We Use It:**
1. Download traffic count points
2. For each candidate site, find nearest traffic count
3. Use AADT to compute normalized traffic index
4. Higher traffic = higher charging demand

**Other Relevant Datasets:**
- Road inventory (road types, lanes)
- Park & Ride facilities
- Transit stations

---

## 5. Points of Interest (POI)

### OpenStreetMap (OSM)
- **API**: Overpass API
- **Use**: Identify nearby amenities
- **Categories**:
  - Retail (shops, restaurants, malls)
  - Employment centers (offices, industrial)
  - Education (schools, universities)
  - Healthcare facilities
  - Recreation

**Integration:**
- Query OSM for POIs within radius of each site
- Compute POI density index
- Higher POI density = more charging demand

### SafeGraph / Foursquare
- Alternative commercial POI datasets (not used in portfolio version)

---

## 6. EV Incentives & Policy Data

### MOR-EV (Massachusetts Offers Rebates for Electric Vehicles)
- **URL**: https://mor-ev.org
- **Official Info**: https://www.mass.gov/info-details/mor-ev-rebate-program
- **Use**: Context on EV adoption incentives
- **Display**: Show rebate amounts in site detail panel

### MassCEC (Massachusetts Clean Energy Center)
- **URL**: https://goclean.masscec.com/ev-rebates-and-incentives/
- **Programs**:
  - MassEVIP: Charging infrastructure rebates
  - Workplace charging programs
  - Multi-unit dwelling programs
  
**Integrated Into:**
- Site detail panel shows relevant incentives
- Scoring considers eligibility factors

---

## 7. Grid & Infrastructure Data

### Electric Utilities
- **Eversource**, **National Grid**: Major MA utilities
- Ideal data (not publicly available):
  - Transformer locations and capacity
  - Distribution line locations
  - Voltage levels
  
**Portfolio Approach:**
- Simplified grid score based on proxies:
  - Parking lot presence
  - Municipal/commercial property
  - Proximity to major roads (as infrastructure proxy)

---

## Data Pipeline Implementation

### Synthetic Data Generation (Current)

For the portfolio project, data is generated using:

1. **Grid-based candidate sites**
   - Regular grid over Worcester bounding box
   - ~500-1000 candidate locations

2. **Simulated demographics**
   - Spatial patterns (higher density near downtown)
   - Realistic distributions
   - Correlation between related features

3. **Simulated traffic**
   - Higher near major corridors
   - Distance decay from downtown
   - Random variation

**See:** `/data/ingest_*.py` scripts for implementation

### Real Data Integration (Future)

To integrate real data:

1. Update `ingest_parcels.py`:
   ```python
   # Load actual Worcester parcel shapefile
   import geopandas as gpd
   parcels = gpd.read_file('data/raw/worcester_parcels.shp')
   # Filter, process, store
   ```

2. Update `ingest_demographics.py`:
   ```python
   # Load MAPC or Census data
   demographics = pd.read_csv('data/raw/mapc_demographics.csv')
   # Join by census tract, normalize
   ```

3. Update `ingest_traffic.py`:
   ```python
   # Load MassDOT traffic counts
   traffic = gpd.read_file('data/raw/massdot_traffic.geojson')
   # Nearest neighbor join to sites
   ```

---

## Data Quality Considerations

### Validation Checks
- Coordinate bounds (lat/lng in MA range)
- Feature ranges (all indexes 0-1)
- Required fields present
- Spatial join quality

### Data Freshness
- Parcels: Updated annually by municipalities
- Demographics: ACS 5-year estimates (2018-2022 latest)
- Traffic: Annual MassDOT updates
- OSM: Continuously updated

### Known Limitations
1. **Parcel data quality varies** by municipality
2. **Traffic counts** not available on all roads
3. **Demographic data** aggregated to census geography (privacy)
4. **OSM completeness** varies by area

---

## Licensing & Attribution

### Public Data
Most MA open data is published under open licenses allowing reuse with attribution.

### Commercial Data
If using commercial datasets (SafeGraph, etc.), comply with licensing terms.

### Attribution
Always cite data sources in published analyses:

```
Data Sources:
- MassGIS Property Tax Parcels (Mass.gov)
- MAPC DataCommon (Metropolitan Area Planning Council)
- MassDOT Traffic Inventory (Massachusetts Department of Transportation)
- OpenStreetMap contributors
```

---

## References

- [Mass.gov Open Data](https://data.mass.gov)
- [MassGIS](https://www.mass.gov/orgs/massgis-bureau-of-geographic-information)
- [MAPC DataCommon](https://datacommon.mapc.org)
- [MassDOT Open Data](https://geo-massdot.opendata.arcgis.com)
- [MOR-EV Program](https://mor-ev.org)
- [MassCEC EV Resources](https://goclean.masscec.com)

---

**Note**: This is a portfolio project. While structured to work with real data, the current implementation uses synthetic data for demonstration purposes.
