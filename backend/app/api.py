from fastapi import APIRouter, HTTPException
from typing import List, Dict
import random
import joblib
import pandas as pd
import os
from . import schemas

router = APIRouter()

# Load model if exists
MODEL_PATH = "models/site_score_model.pkl"
model = None
if os.path.exists(MODEL_PATH):
    try:
        model = joblib.load(MODEL_PATH)
        print(f"Loaded ML model from {MODEL_PATH}")
    except Exception as e:
        print(f"Failed to load model: {e}")

# Mock data
MOCK_CITIES = [
    {
        "slug": "worcester",
        "name": "Worcester, MA",
        "bbox": [42.20, -71.85, 42.35, -71.75] # Approx bounding box
    }
]

# Generate some mock sites for Worcester
MOCK_SITES = []
for i in range(100):
    lat = 42.26 + (random.random() - 0.5) * 0.1
    lng = -71.80 + (random.random() - 0.5) * 0.1
    traffic = random.random()
    pop = random.random()
    
    score_demand = 0.4 * traffic + 0.3 * pop + 0.3 * random.random()
    score_equity = random.random()
    score_traffic = traffic
    score_grid = 0.5
    
    score_overall = 0.45 * score_demand + 0.35 * score_equity + 0.20 * score_grid
    
    MOCK_SITES.append({
        "id": f"site-{i}",
        "lat": lat,
        "lng": lng,
        "score_overall": round(score_overall * 100, 1),
        "score_demand": round(score_demand * 100, 1),
        "score_equity": round(score_equity * 100, 1),
        "score_traffic": round(score_traffic * 100, 1),
        "score_grid": round(score_grid * 100, 1),
        "daily_kwh_estimate": round(score_overall * 50, 1), # simple mock correlation
        "location_label": f"Block {i}",
        "features": {
            "traffic_index": traffic,
            "pop_density_index": pop,
            "renters_share": random.random(),
            "income_index": random.random(),
            "poi_index": random.random()
        }
    })

@router.get("/cities", response_model=List[schemas.City])
def get_cities():
    return MOCK_CITIES

@router.get("/sites", response_model=List[schemas.SiteBase])
def get_sites(city: str):
    if city != "worcester":
        return []
    return MOCK_SITES

@router.get("/site/{site_id}", response_model=schemas.SiteDetail)
def get_site(site_id: str):
    site = next((s for s in MOCK_SITES if s["id"] == site_id), None)
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")
    
    # Add notes for detail view
    site_with_notes = site.copy()
    site_with_notes["notes"] = "Eligible for MOR-EV fleet rebates. Located in an Environmental Justice community."
    return site_with_notes

@router.post("/predict", response_model=schemas.PredictionOutput)
def predict_score(input_data: schemas.PredictionInput):
    # ML Model Prediction
    if model:
        # Create dataframe from input
        features = pd.DataFrame([{
            'traffic_index': input_data.traffic_index,
            'pop_density_index': input_data.pop_density_index,
            'renters_share': input_data.renters_share,
            'income_index': input_data.income_index,
            'poi_index': input_data.poi_index
        }])
        
        # Predict daily kWh
        daily_kwh = float(model.predict(features)[0])
    else:
        # Fallback to heuristic
        # expected_sessions ≈ 4 + 8*traffic + 6*pop
        sessions = 4 + 8 * input_data.traffic_index + 6 * input_data.pop_density_index
        daily_kwh = sessions * 25

    # Heuristic scoring (transparent)
    # score_demand = 0.4 * traffic + 0.3 * pop + 0.3 * poi
    score_demand = 0.4 * input_data.traffic_index + 0.3 * input_data.pop_density_index + 0.3 * input_data.poi_index
    
    # score_equity = 0.5 * (1 - income) + 0.5 * renters
    score_equity = 0.5 * (1 - input_data.income_index) + 0.5 * input_data.renters_share
    
    score_traffic = input_data.traffic_index
    score_grid = 0.5 # constant for now
    
    score_overall = 0.45 * score_demand + 0.35 * score_equity + 0.20 * score_grid
    
    return {
        "score_overall": round(score_overall * 100, 1),
        "daily_kwh_estimate": round(daily_kwh, 1),
        "component_scores": {
            "score_demand": round(score_demand * 100, 1),
            "score_equity": round(score_equity * 100, 1),
            "score_traffic": round(score_traffic * 100, 1),
            "score_grid": round(score_grid * 100, 1)
        }
    }
