#!/bin/bash

# MA EV ChargeMap - Data Pipeline Runner
# 
# This script runs the complete data pipeline to generate Worcester EV charging
# site data from scratch.
#
# Steps:
# 1. Generate candidate site locations (grid)
# 2. Add demographic features
# 3. Add traffic features  
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

echo ""
echo "Step 1/4: Generating candidate site locations..."
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
echo "You can now:"
echo "  - Start the API: cd ../backend && python -m app.main"
echo "  - View data in notebooks: cd ../notebooks"
echo ""
