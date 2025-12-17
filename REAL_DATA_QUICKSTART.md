# Real Data Quick Start ⚡

Get MA EV ChargeMap running with **real OpenStreetMap and US Census data** in under 10 minutes!

---

## 🎯 What You'll Get

- **200-500 real buildings** from OpenStreetMap (vs. uniform grid)
- **1000-2000 real POIs** (shops, restaurants, schools, etc.)
- **Real census demographics** (income, renters, population)
- **Actual road network** for traffic estimation
- **Verifiable data** that anyone can check

---

## ⚡ Quick Start

### Step 1: Clone and Setup (if not done)

```bash
git clone <your-repo>
cd ma-ev-chargemap
./infra/dev-setup.sh  # Sets up Docker environment
```

### Step 2: Download Real Data

```bash
cd data
python fetch_real_data.py
```

**What happens**: Script downloads from public APIs:
- OpenStreetMap Overpass API (buildings, POIs, roads)
- US Census Bureau API (demographics)

**Time**: 2-5 minutes  
**No authentication required** - all public APIs!

**Output**:
```
📦 Fetching building data from OpenStreetMap...
  ✓ Fetched 342 buildings

🏪 Fetching POI data from OpenStreetMap...
  ✓ Fetched 1,847 POIs

🛣️ Fetching road network from OpenStreetMap...
  ✓ Fetched 8,429 road segments

👥 Fetching demographic data from US Census Bureau...
  ✓ Fetched data for 67 census tracts

✓ All data saved to: data/raw/
```

### Step 3: Run Data Pipeline

```bash
./run_pipeline.sh
```

**What happens**: Processes real data into scored sites:
1. Loads 342 real Worcester buildings (not synthetic grid)
2. Computes POI density from 1,847 real locations
3. Estimates traffic from actual road classifications
4. Applies Census demographics

**Time**: ~15-20 seconds

**Output**:
```
✓ Using 342 real building locations from OSM
✓ 47 identified as parking facilities
✓ Used real data: POI=True, Census=True
```

### Step 4: Start the App

```bash
cd ..
docker-compose up
```

Access at: http://localhost:3000

---

## 🔍 Verifying Real Data

### In the UI

1. Open http://localhost:3000
2. Click "Explore Worcester"
3. Look at site markers - they cluster around **real commercial areas**
4. Click a site - check the parcel ID:
   - **Real**: `OSM-12345678` (OpenStreetMap ID)
   - **Synthetic**: `WORC-GRID-0001`

### In the Database

```bash
docker-compose exec db psql -U evcharge -d evcharge

-- Count sites
SELECT COUNT(*) FROM sites;

-- Check for real OSM IDs
SELECT parcel_id, location_label, parking_lot_flag 
FROM sites 
LIMIT 10;

-- Sites with real parking data
SELECT COUNT(*) FROM sites WHERE parking_lot_flag = 1;
```

### Check Downloaded Files

```bash
ls -lh data/raw/*.csv
head data/raw/worcester_buildings_osm.csv
```

---

## 📊 Real Data Impact

### Before (Synthetic Grid)
- ✓ Uniform coverage
- ✗ No relationship to actual buildings
- ✗ Random POI distribution
- ✗ Estimated traffic patterns

### After (Real Data)
- ✓ Actual building locations
- ✓ Real commercial/retail sites
- ✓ True POI clustering
- ✓ Road-classification-based traffic
- ✓ Census-verified demographics

---

## 🎓 Portfolio Value

**Resume/LinkedIn**:
> "Integrated **OpenStreetMap** and **US Census Bureau** public APIs to process 2000+ real points of interest and 500+ building footprints for EV charging site analysis"

**Interview Talking Points**:
- "I integrated two public APIs without authentication"
- "Built robust error handling with automatic fallback"
- "Processed geospatial data from OpenStreetMap"
- "Used Census API for real demographic data"
- "Anyone can verify the data sources"

---

## 🔧 Troubleshooting

### "Request timeout" on OSM
**Cause**: Overpass API is busy  
**Solution**: Wait 2-3 minutes and try again. The script has built-in delays.

### "Census API slow"
**Cause**: Census API can be slow during business hours  
**Solution**: Be patient (30-60s timeout) or run during off-hours

### Want to re-download?
```bash
rm data/raw/*.csv
python fetch_real_data.py
```

### Prefer synthetic data?
```bash
rm data/raw/*.csv  # Remove real data
./run_pipeline.sh  # Will automatically use synthetic
```

---

## 🌟 Data Sources

### OpenStreetMap
- **License**: ODbL (Open Database License)
- **Attribution**: © OpenStreetMap contributors
- **Link**: https://www.openstreetmap.org/
- **Coverage**: Excellent for Worcester, MA

### US Census Bureau
- **License**: Public domain
- **Attribution**: Not required (but appreciated)
- **Link**: https://www.census.gov/
- **Data**: 2021 5-year ACS estimates

### Why These Sources?
✅ **Free** - No API keys or fees  
✅ **Public** - Anyone can verify  
✅ **Updated** - OSM daily, Census every 5 years  
✅ **Reputable** - Authoritative sources  
✅ **Portfolio-Ready** - Shows real data skills  

---

## 📈 Next Steps

1. **Run the app** - See real building locations
2. **Check clustering** - Notice sites near actual commercial areas
3. **Compare scores** - Real POI data creates more variation
4. **Take screenshots** - Show in portfolio
5. **Update resume** - Highlight real data integration

---

## 💡 Pro Tips

1. **Cache the data**: Downloaded files can be reused  
2. **Check data quality**: Look at raw CSVs to understand the data  
3. **Document your choice**: Mention real data sources in cover letters  
4. **Show the fallback**: Demonstrates robust error handling  
5. **Compare results**: Show both real and synthetic for comparison  

---

**Ready?** Run `python fetch_real_data.py` and see your project come to life with real data! 🚀

---

## 📞 Support

- **Overpass API Status**: https://overpass-api.de/api/status
- **Census API**: https://www.census.gov/data/developers.html
- **OSM Help**: https://help.openstreetmap.org/

**Documentation**: See `data/README_REAL_DATA.md` for full details
