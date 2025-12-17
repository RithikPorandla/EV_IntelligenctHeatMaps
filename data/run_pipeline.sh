#!/bin/bash

# MA EV ChargeMap - Data Pipeline Runner
# 
# This script runs the complete data pipeline to generate Worcester EV charging
# site data from real or synthetic sources.
#
# Steps:
# 0. (Optional) Fetch real data from OpenStreetMap & Census
# 1. Load candidate site locations (OSM buildings or grid)
# 2. Add demographic features (Census + OSM POIs or synthetic)
# 3. Add traffic features (OSM roads or synthetic)
# 4. Compute final scores

set -e  # Exit on error

echo "=========================================="
echo "MA EV ChargeMap - Data Pipeline"
echo "=========================================="
echo ""

# Check if virtual environment exists
if [ ! -d "../backend/venv" ]; then
    echo "⚠️  No virtual environment found at backend/venv"
    echo "   Please create one first:"
    echo "   cd backend && python -m venv venv && source venv/bin/activate && pip install -r requirements.txt"
    exit 1
fi

# Activate virtual environment
echo "Activating Python environment..."
source ../backend/venv/bin/activate

# Check for real data
echo ""
echo "Checking for real data sources..."
if [ -f "raw/worcester_buildings_osm.csv" ]; then
    echo "  ✓ Found real OSM building data"
    USE_REAL=true
else
    echo "  ℹ No real data found - will use synthetic data"
    echo "  ℹ To download real data, run: python fetch_real_data.py"
    USE_REAL=false
fi

# Offer to fetch real data if not present
if [ "$USE_REAL" = false ]; then
    echo ""
    echo "Would you like to download real data now? (y/n)"
    read -t 10 -n 1 response || response='n'
    echo ""
    if [[ "$response" =~ ^[Yy]$ ]]; then
        echo "Fetching real data from OpenStreetMap and Census..."
        python fetch_real_data.py
        USE_REAL=true
    fi
fi

echo ""
echo "Step 1/4: Loading candidate site locations..."
echo "----------------------------------------"
python ingest_parcels.py

echo ""
echo "Step 2/4: Adding demographic features..."
echo "----------------------------------------"
python ingest_demographics.py

echo ""
echo "Step 3/4: Adding traffic features..."
echo "----------------------------------------"
python ingest_traffic.py

echo ""
echo "Step 4/4: Computing final scores..."
echo "----------------------------------------"
python build_scores.py

echo ""
echo "=========================================="
echo "✓ Pipeline complete!"
echo "=========================================="
echo ""
if [ "$USE_REAL" = true ]; then
    echo "📊 Used REAL data from:"
    echo "  - OpenStreetMap (buildings, POIs, roads)"
    echo "  - US Census Bureau (demographics)"
else
    echo "📊 Used SYNTHETIC data for demonstration"
    echo "  ℹ Run 'python fetch_real_data.py' to use real data"
fi
echo ""
echo "You can now:"
echo "  - Start the API: cd ../backend && python -m app.main"
echo "  - View data in notebooks: cd ../notebooks"
echo "  - View data docs: cat README_REAL_DATA.md"
echo ""
