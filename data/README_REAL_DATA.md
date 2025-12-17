# Using Real Open-Source Datasets

This project now supports **real, publicly available datasets** from multiple sources!

## 🌍 Data Sources

### 1. OpenStreetMap (OSM)
**Free, no authentication required**

- **Buildings**: Commercial, retail, public buildings, parking facilities
- **Points of Interest**: Shops, restaurants, offices, schools, hospitals
- **Roads**: Major road network with classifications

**API**: Overpass API (https://overpass-api.de/)

### 2. US Census Bureau
**Free, public API (no key required for basic queries)**

- **Demographics**: Population, household income
- **Housing**: Renter vs. owner-occupied units
- **Geography**: Census tract boundaries

**API**: https://api.census.gov/

---

## 📥 Fetching Real Data

### Step 1: Run the Data Fetcher

```bash
cd /workspace/data
python fetch_real_data.py
```

This script will:
- Download Worcester building footprints from OSM (→ candidate sites)
- Download POI data from OSM (→ POI density calculation)
- Download road network from OSM (→ traffic estimation)
- Download Census demographic data (→ income, renters, population)

**Time**: 2-5 minutes depending on internet speed  
**Size**: ~5-10 MB total

### Step 2: Run the Data Pipeline

```bash
./run_pipeline.sh
```

The pipeline scripts automatically detect and use real data:
- `ingest_parcels.py` - Uses OSM buildings if available, falls back to grid
- `ingest_demographics.py` - Uses OSM POIs and Census data if available
- `ingest_traffic.py` - Uses OSM roads if available
- `build_scores.py` - Works with any data source

---

## 🔍 What You Get with Real Data

### OSM Buildings (~200-500 locations)
- **Actual building locations** instead of uniform grid
- **Parking facilities** automatically identified
- **Building types** (commercial, retail, public)
- **Real addresses** where available

### OSM POIs (~1000-2000 points)
- **Actual shops, restaurants, offices**
- Used to compute **real POI density** for each site
- More accurate than synthetic data

### OSM Roads (~5000-10000 segments)
- **Classified roads** (motorway, primary, secondary)
- Used for **traffic estimation** by road type
- Better than distance-based heuristics

### Census Data (~50-80 tracts)
- **Real population** by census tract
- **Actual median income** data
- **True renter percentages**
- From 2021 5-year ACS estimates (most recent stable data)

---

## 📊 Data Quality

### Advantages of Real Data
✅ **Credible**: Actual locations from authoritative sources  
✅ **Verifiable**: Anyone can check the source data  
✅ **Current**: OSM updated continuously, Census every 5 years  
✅ **Portfolio-Ready**: Shows ability to work with real public datasets  

### Limitations
⚠️ **OSM Completeness**: Varies by area (Worcester has good coverage)  
⚠️ **Census Aggregation**: Data at tract level, not individual sites  
⚠️ **Traffic Data**: Estimated from road classifications, not actual counts  

**Note**: For production, would integrate:
- MassDOT actual traffic counts
- MAPC detailed demographic layers
- Worcester city parcel ownership data

---

## 🔄 Fallback Behavior

If real data download fails, the pipeline **automatically falls back** to synthetic data:

```
⚠️  Real data not available, using synthetic approach
  ℹ Run 'python fetch_real_data.py' to download real data
```

This ensures the project always works, even without internet access.

---

## 🌐 API Rate Limits & Best Practices

### Overpass API (OSM)
- **Rate Limit**: ~2 requests/second
- **Timeout**: 60 seconds per query
- **Best Practice**: Script includes 2-second delays between requests

### Census API
- **Rate Limit**: None for public endpoints
- **Timeout**: Can be slow (30-120 seconds)
- **Best Practice**: Download once, cache locally

**Important**: The `fetch_real_data.py` script is designed to be **run once** and reuse the downloaded data.

---

## 📁 Downloaded Files

After running `fetch_real_data.py`, you'll have:

```
data/raw/
├── worcester_buildings_osm.csv      # Building locations
├── worcester_pois_osm.csv           # Points of interest
├── worcester_roads_osm.csv          # Road network
├── worcester_census_tracts.csv      # Demographics
└── census_tracts.zip                # Tract boundaries (optional)
```

**Sizes**:
- Buildings: ~50-100 KB
- POIs: ~100-200 KB
- Roads: ~1-2 MB
- Census: ~10-20 KB

---

## 🧪 Verifying Real Data

### Check Downloaded Files

```bash
cd data/raw
ls -lh *.csv
head worcester_buildings_osm.csv
```

### Check Database After Pipeline

```bash
# Connect to database
docker-compose exec db psql -U evcharge -d evcharge

# Count sites
SELECT COUNT(*) FROM sites;

# Check for real OSM IDs (vs. synthetic WORC-GRID-*)
SELECT parcel_id, location_label FROM sites LIMIT 10;

# Check parking flags from OSM
SELECT COUNT(*) FROM sites WHERE parking_lot_flag = 1;

# View POI density distribution
SELECT 
  AVG(poi_index),
  MIN(poi_index),
  MAX(poi_index)
FROM sites;
```

---

## 🎯 Portfolio Value

**Before**: "I built a tool with synthetic data"  
**After**: "I integrated real public datasets from OpenStreetMap and US Census Bureau"

**Talking Points**:
- "Downloaded and processed 1000+ real POIs from OpenStreetMap"
- "Integrated US Census demographic data at census tract level"
- "Built robust pipeline with automatic fallback if data unavailable"
- "Demonstrated ability to work with public APIs and geospatial data"

---

## 🔧 Troubleshooting

### Overpass API Timeout
```
Error: Overpass API timeout
```
**Solution**: The API is busy. Wait a few minutes and try again.

### Census API Slow
```
Error: Census API timeout
```
**Solution**: Census API can be slow. The script has 30s timeout. Try again or use cached data.

### No Internet Connection
**Solution**: Use synthetic data (automatic fallback). The project works offline!

### "scipy not found"
**Solution**: 
```bash
cd /workspace/backend
source venv/bin/activate
pip install scipy
```

---

## 📚 Data Attribution

When using this project, please attribute:

**OpenStreetMap**:
- Data © OpenStreetMap contributors, ODbL license
- https://www.openstreetmap.org/copyright

**US Census Bureau**:
- Data from US Census Bureau, American Community Survey
- Public domain, no attribution required
- https://www.census.gov/

---

## 🚀 Next Steps

1. **Run data fetcher**: `python fetch_real_data.py`
2. **Run pipeline**: `./run_pipeline.sh`
3. **Start app**: See main README
4. **View results**: Check for real locations in the map!

**Bonus**: Compare scores with real vs. synthetic data:
- More variation in POI density
- Clustering around actual commercial areas
- Parking lots get higher grid scores

---

**Status**: ✅ Real data integration complete!

The project now uses **publicly available, verifiable datasets** while maintaining the flexibility to work with synthetic data for demonstrations.
