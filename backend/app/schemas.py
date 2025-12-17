from pydantic import BaseModel
from typing import List, Optional

class City(BaseModel):
    slug: str
    name: str
    bbox: List[float]  # [min_lat, min_lng, max_lat, max_lng] or similar

class SiteBase(BaseModel):
    id: str
    lat: float
    lng: float
    score_overall: float
    score_demand: float
    score_equity: float
    score_traffic: float
    score_grid: float
    daily_kwh_estimate: float
    location_label: Optional[str] = None

class SiteDetail(SiteBase):
    features: dict
    notes: Optional[str] = None

class PredictionInput(BaseModel):
    traffic_index: float
    pop_density_index: float
    renters_share: float
    income_index: float
    poi_index: float

class PredictionOutput(BaseModel):
    score_overall: float
    daily_kwh_estimate: float
    component_scores: dict
