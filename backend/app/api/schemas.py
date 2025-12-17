"""
Pydantic schemas for API request/response validation.
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any


class CityInfo(BaseModel):
    """Information about a supported city."""
    slug: str = Field(..., description="URL-friendly city identifier")
    name: str = Field(..., description="Full city name")
    state: str = Field(default="MA", description="State code")
    bbox: List[float] = Field(..., description="Bounding box [west, south, east, north]")
    center: List[float] = Field(..., description="Center coordinates [lat, lng]")


class SiteFeatures(BaseModel):
    """Site feature indexes."""
    traffic_index: float = Field(ge=0.0, le=1.0)
    pop_density_index: float = Field(ge=0.0, le=1.0)
    renters_share: float = Field(ge=0.0, le=1.0)
    income_index: float = Field(ge=0.0, le=1.0)
    poi_index: float = Field(ge=0.0, le=1.0)
    parking_lot_flag: int = Field(ge=0, le=1)
    municipal_parcel_flag: int = Field(ge=0, le=1)


class SiteScores(BaseModel):
    """Site opportunity scores."""
    demand: float = Field(..., description="Demand score (0-100)")
    equity: float = Field(..., description="Equity score (0-100)")
    traffic: float = Field(..., description="Traffic score (0-100)")
    grid: float = Field(..., description="Grid readiness score (0-100)")
    overall: float = Field(..., description="Overall opportunity score (0-100)")


class SiteSummary(BaseModel):
    """Summary information for a site (used in list views)."""
    id: int
    city: str
    lat: float
    lng: float
    location_label: Optional[str] = None
    scores: SiteScores
    daily_kwh_estimate: float


class SiteDetail(SiteSummary):
    """Detailed information for a site."""
    parcel_id: Optional[str] = None
    features: SiteFeatures


class SitesResponse(BaseModel):
    """Response for sites list endpoint."""
    type: str = "FeatureCollection"
    features: List[Dict]
    count: int


class PredictionRequest(BaseModel):
    """Request for ML prediction endpoint."""
    traffic_index: float = Field(ge=0.0, le=1.0, description="Traffic volume index")
    pop_density_index: float = Field(ge=0.0, le=1.0, description="Population density index")
    renters_share: float = Field(ge=0.0, le=1.0, description="Fraction of renters")
    income_index: float = Field(ge=0.0, le=1.0, description="Income level index")
    poi_index: float = Field(ge=0.0, le=1.0, description="POI density index")
    parking_lot_flag: int = Field(default=0, ge=0, le=1, description="Has parking lot")
    municipal_parcel_flag: int = Field(default=0, ge=0, le=1, description="Is municipal property")


class PredictionResponse(BaseModel):
    """Response for ML prediction endpoint."""
    scores: SiteScores
    daily_kwh_estimate: float
    model_info: Dict[str, Any]


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    version: str
    database: str
