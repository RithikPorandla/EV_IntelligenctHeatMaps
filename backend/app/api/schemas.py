from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class CityOut(BaseModel):
    slug: str
    name: str
    bbox: dict[str, float] = Field(
        ..., description="Bounding box in WGS84: {west,south,east,north}"
    )


class SiteOut(BaseModel):
    id: str
    city_slug: str

    lat: float
    lng: float

    score_overall: float
    score_demand: float
    score_equity: float
    score_traffic: float
    score_grid: float

    daily_kwh_estimate: float

    location_label: str | None = None
    parcel_id: str | None = None


class SiteDetailOut(SiteOut):
    features: dict[str, float]
    notes: list[str] = []


class PredictIn(BaseModel):
    traffic_index: float = Field(..., ge=0, le=1)
    pop_density_index: float = Field(..., ge=0, le=1)
    renters_share: float = Field(..., ge=0, le=1)
    income_index: float = Field(..., ge=0, le=1)
    poi_index: float = Field(..., ge=0, le=1)


class PredictOut(BaseModel):
    predicted_daily_kwh: float
    scores: dict[str, float]
    model: dict[str, Any]
