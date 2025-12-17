from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.models.site import Site, SiteSchema, CityInfo
from app.services.scoring import ScoringService

router = APIRouter()

CITIES = {
    "worcester": {
        "slug": "worcester",
        "name": "Worcester, MA",
        "center": [42.2626, -71.8023],
        "zoom": 13
    }
}

@router.get("/cities", response_model=List[CityInfo])
def get_cities():
    return list(CITIES.values())

@router.get("/sites", response_model=List[SiteSchema])
def get_sites(city: str, db: Session = Depends(get_db)):
    if city not in CITIES:
        raise HTTPException(status_code=404, detail="City not supported")
    
    sites = db.query(Site).filter(Site.city_slug == city).all()
    return sites

@router.get("/site/{site_id}", response_model=SiteSchema)
def get_site(site_id: int, db: Session = Depends(get_db)):
    site = db.query(Site).filter(Site.id == site_id).first()
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")
    return site

@router.post("/predict")
def predict_score(
    traffic_index: float,
    pop_density_index: float,
    renters_share: float,
    income_index: float,
    poi_index: float
):
    """
    On-the-fly scoring for arbitrary feature values.
    """
    scores = ScoringService.calculate_scores(
        traffic_index=traffic_index,
        pop_density_index=pop_density_index,
        renters_share=renters_share,
        income_index=income_index,
        poi_index=poi_index
    )
    kwh = ScoringService.estimate_daily_kwh(traffic_index, pop_density_index)
    scores["daily_kwh_estimate"] = kwh
    return scores
