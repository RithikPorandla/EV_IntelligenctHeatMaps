from sqlalchemy import Column, Integer, String, Float, Boolean, JSON
from sqlalchemy.orm import declarative_base
from pydantic import BaseModel
from typing import Optional, List

Base = declarative_base()

class Site(Base):
    __tablename__ = "sites"

    id = Column(Integer, primary_key=True, index=True)
    city_slug = Column(String, index=True)
    parcel_id = Column(String, nullable=True)
    address = Column(String, nullable=True)
    lat = Column(Float)
    lng = Column(Float)
    
    # Input Features (normalized or raw)
    traffic_index = Column(Float, default=0.0)
    pop_density_index = Column(Float, default=0.0)
    renters_share = Column(Float, default=0.0)
    income_index = Column(Float, default=0.0)
    poi_index = Column(Float, default=0.0)
    ev_incentive_flag = Column(Boolean, default=False)
    
    # Computed Scores
    score_demand = Column(Float, default=0.0)
    score_equity = Column(Float, default=0.0)
    score_traffic = Column(Float, default=0.0)
    score_grid = Column(Float, default=0.0)
    score_overall = Column(Float, default=0.0)
    
    # Estimates
    daily_kwh_estimate = Column(Float, default=0.0)

class SiteSchema(BaseModel):
    id: int
    city_slug: str
    parcel_id: Optional[str] = None
    address: Optional[str] = None
    lat: float
    lng: float
    score_overall: float
    score_demand: float
    score_equity: float
    score_traffic: float
    score_grid: float
    daily_kwh_estimate: float
    
    class Config:
        from_attributes = True

class CityInfo(BaseModel):
    slug: str
    name: str
    center: List[float]  # [lat, lng]
    zoom: int
