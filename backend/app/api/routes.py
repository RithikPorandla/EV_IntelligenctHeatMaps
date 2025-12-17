"""
API route handlers for MA EV ChargeMap.
"""
import json
from pathlib import Path
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.models.site import Site
from app.api.schemas import (
    CityInfo, SiteDetail, SitesResponse, PredictionRequest, PredictionResponse, HealthResponse
)
from app.services.scoring import ScoringService
from app.services.ml_predictor import predictor
from app.config import settings

router = APIRouter()


# City data (could be moved to database in future)
CITIES = {
    "worcester": {
        "slug": "worcester",
        "name": "Worcester",
        "state": "MA",
        "bbox": [-71.8744, 42.2084, -71.7277, 42.3126],  # [west, south, east, north]
        "center": [42.2626, -71.8023]  # [lat, lng]
    }
}

# Incentives config (static JSON for v1)
INCENTIVES_PATH = Path(__file__).resolve().parents[2] / "config" / "incentives.json"
try:
    INCENTIVES_CONFIG = json.loads(INCENTIVES_PATH.read_text())
except Exception:
    INCENTIVES_CONFIG = {
        "title": "Massachusetts EV Charging Incentives",
        "description": "Incentives config file missing or unreadable",
        "programs": [],
    }


@router.get("/health", response_model=HealthResponse)
def health_check(db: Session = Depends(get_db)):
    """
    Health check endpoint.
    
    Returns API status and database connectivity.
    """
    try:
        # Test database connection
        db.execute("SELECT 1")
        db_status = "connected"
    except Exception as e:
        db_status = f"error: {str(e)}"
    
    return {
        "status": "healthy",
        "version": settings.version,
        "database": db_status
    }


@router.get("/cities", response_model=List[CityInfo])
def get_cities():
    """
    Get list of supported cities.
    
    Returns information about all cities with available data.
    Currently supports Worcester, MA as pilot city.
    """
    return [CityInfo(**city) for city in CITIES.values()]


@router.get("/incentives")
def get_incentives():
    """
    Get Massachusetts EV incentive context (human-readable).

    Used by the frontend site detail panel to provide program guidance.
    """
    return INCENTIVES_CONFIG


@router.get("/cities/{city_slug}", response_model=CityInfo)
def get_city(city_slug: str):
    """
    Get information about a specific city.
    
    Args:
        city_slug: URL-friendly city identifier (e.g., 'worcester')
    
    Returns:
        City information including bounding box and center coordinates
    
    Raises:
        404: If city not found
    """
    city = CITIES.get(city_slug.lower())
    if not city:
        raise HTTPException(status_code=404, detail=f"City '{city_slug}' not found")
    return CityInfo(**city)


@router.get("/sites", response_model=SitesResponse)
def get_sites(
    city: str = Query(..., description="City slug (e.g., 'worcester')"),
    min_score: Optional[float] = Query(None, ge=0, le=100, description="Minimum overall score filter"),
    limit: Optional[int] = Query(1000, ge=1, le=10000, description="Maximum number of sites to return"),
    db: Session = Depends(get_db)
):
    """
    Get candidate EV charging sites for a city.
    
    Returns sites as GeoJSON FeatureCollection for easy map visualization.
    
    Args:
        city: City slug (e.g., 'worcester')
        min_score: Optional minimum overall score filter (0-100)
        limit: Maximum number of sites to return (default 1000)
    
    Returns:
        GeoJSON FeatureCollection with site data
    
    Raises:
        404: If city not found
    """
    # Validate city
    if city.lower() not in CITIES:
        raise HTTPException(status_code=404, detail=f"City '{city}' not found")
    
    # Build query
    query = db.query(Site).filter(Site.city == city.lower())
    
    # Apply score filter if provided
    if min_score is not None:
        query = query.filter(Site.score_overall >= min_score)
    
    # Order by score (best first) and apply limit
    query = query.order_by(Site.score_overall.desc()).limit(limit)
    
    # Execute query
    sites = query.all()
    
    # Convert to GeoJSON features
    features = [site.to_geojson_feature() for site in sites]
    
    return {
        "type": "FeatureCollection",
        "features": features,
        "count": len(features)
    }


@router.get("/sites/{site_id}", response_model=SiteDetail)
def get_site(site_id: int, db: Session = Depends(get_db)):
    """
    Get detailed information for a specific site.
    
    Args:
        site_id: Unique site identifier
    
    Returns:
        Complete site information including features and scores
    
    Raises:
        404: If site not found
    """
    site = db.query(Site).filter(Site.id == site_id).first()
    
    if not site:
        raise HTTPException(status_code=404, detail=f"Site {site_id} not found")
    
    return SiteDetail(**site.to_dict())


@router.get("/site/{site_id}", response_model=SiteDetail)
def get_site_compat(site_id: int, db: Session = Depends(get_db)):
    """
    Compatibility alias for the v1 spec:
    `GET /api/site/{id}`.

    The canonical endpoint in this codebase is `GET /api/sites/{id}`.
    """
    return get_site(site_id=site_id, db=db)


@router.post("/predict", response_model=PredictionResponse)
def predict_site_scores(request: PredictionRequest):
    """
    Predict scores and demand for a hypothetical location.
    
    Uses the trained ML model (or heuristic fallback) to estimate
    charging opportunity for a location with given features.
    
    Useful for:
    - Evaluating new candidate locations
    - Understanding feature importance
    - "What-if" scenario analysis
    
    Args:
        request: Site features (all indexes 0-1 normalized)
    
    Returns:
        Predicted scores and daily kWh estimate
    """
    # Convert request to feature dictionary
    features = request.model_dump()
    
    # Compute heuristic scores
    scores = ScoringService.compute_all_scores(features)
    
    # Get ML prediction for daily kWh (may fall back to heuristic)
    ml_kwh = predictor.predict_daily_kwh(features)
    
    # Use ML prediction if available, otherwise use heuristic
    if predictor.model is not None:
        daily_kwh = ml_kwh
    else:
        daily_kwh = scores['daily_kwh_estimate']
    
    return PredictionResponse(
        scores={
            "demand": round(scores['score_demand'], 1),
            "equity": round(scores['score_equity'], 1),
            "traffic": round(scores['score_traffic'], 1),
            "grid": round(scores['score_grid'], 1),
            "overall": round(scores['score_overall'], 1),
        },
        daily_kwh_estimate=round(daily_kwh, 1),
        model_info=predictor.get_model_info()
    )


@router.get("/stats/{city_slug}")
def get_city_stats(city_slug: str, db: Session = Depends(get_db)):
    """
    Get summary statistics for a city.
    
    Args:
        city_slug: City identifier
    
    Returns:
        Statistical summary of sites in the city
    
    Raises:
        404: If city not found
    """
    # Validate city
    if city_slug.lower() not in CITIES:
        raise HTTPException(status_code=404, detail=f"City '{city_slug}' not found")
    
    # Get all sites for city
    sites = db.query(Site).filter(Site.city == city_slug.lower()).all()
    
    if not sites:
        return {
            "city": city_slug,
            "total_sites": 0,
            "message": "No sites found for this city"
        }
    
    # Calculate statistics
    scores = [s.score_overall for s in sites]
    demands = [s.daily_kwh_estimate for s in sites]
    
    # Get top sites
    top_sites = sorted(sites, key=lambda s: s.score_overall, reverse=True)[:10]
    
    return {
        "city": city_slug,
        "total_sites": len(sites),
        "score_stats": {
            "min": round(min(scores), 1),
            "max": round(max(scores), 1),
            "mean": round(sum(scores) / len(scores), 1),
        },
        "demand_stats": {
            "total_daily_kwh": round(sum(demands), 0),
            "mean_daily_kwh": round(sum(demands) / len(demands), 1),
        },
        "top_sites": [
            {
                "id": s.id,
                "location_label": s.location_label,
                "score_overall": round(s.score_overall, 1),
                "daily_kwh_estimate": round(s.daily_kwh_estimate, 1),
            }
            for s in top_sites
        ]
    }
