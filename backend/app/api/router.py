from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query

from app.api.schemas import CityOut, PredictIn, PredictOut, SiteDetailOut, SiteOut
from app.services.cities import SUPPORTED_CITIES, get_city
from app.services.incentives import incentives_note
from app.services.ml_model import load_or_train_model
from app.services.scoring import compute_all_scores
from app.services.site_repository import get_site_by_id, get_sites_for_city

router = APIRouter(prefix="/api")


@router.get("/cities", response_model=list[CityOut])
def list_cities() -> list[CityOut]:
    return [
        CityOut(
            slug=c.slug,
            name=c.name,
            bbox={"west": c.west, "south": c.south, "east": c.east, "north": c.north},
        )
        for c in SUPPORTED_CITIES
    ]


@router.get("/sites", response_model=list[SiteOut])
def list_sites(
    city: str = Query(..., description="City slug, e.g. worcester"),
    min_score: float | None = Query(None, ge=0, le=100, description="Optional minimum overall score"),
) -> list[SiteOut]:
    c = get_city(city)
    if not c:
        raise HTTPException(status_code=404, detail=f"Unsupported city: {city}")

    sites = get_sites_for_city(c)
    if min_score is not None:
        sites = [s for s in sites if s.score_overall >= float(min_score)]

    return [
        SiteOut(
            id=s.id,
            city_slug=s.city_slug,
            lat=s.lat,
            lng=s.lng,
            score_overall=s.score_overall,
            score_demand=s.score_demand,
            score_equity=s.score_equity,
            score_traffic=s.score_traffic,
            score_grid=s.score_grid,
            daily_kwh_estimate=s.daily_kwh_estimate,
            location_label=s.location_label,
            parcel_id=s.parcel_id,
        )
        for s in sites
    ]


@router.get("/site/{site_id}", response_model=SiteDetailOut)
def site_detail(site_id: str, city: str = Query(..., description="City slug")) -> SiteDetailOut:
    c = get_city(city)
    if not c:
        raise HTTPException(status_code=404, detail=f"Unsupported city: {city}")

    s = get_site_by_id(c, site_id)
    if not s:
        raise HTTPException(status_code=404, detail=f"Unknown site id: {site_id}")

    return SiteDetailOut(
        id=s.id,
        city_slug=s.city_slug,
        lat=s.lat,
        lng=s.lng,
        score_overall=s.score_overall,
        score_demand=s.score_demand,
        score_equity=s.score_equity,
        score_traffic=s.score_traffic,
        score_grid=s.score_grid,
        daily_kwh_estimate=s.daily_kwh_estimate,
        location_label=s.location_label,
        parcel_id=s.parcel_id,
        features={
            "traffic_index": s.traffic_index,
            "pop_density_index": s.pop_density_index,
            "renters_share": s.renters_share,
            "income_index": s.income_index,
            "poi_index": s.poi_index,
        },
        notes=[incentives_note()],
    )


@router.post("/predict", response_model=PredictOut)
def predict(payload: PredictIn) -> PredictOut:
    features = payload.model_dump()

    heuristic_scores = compute_all_scores(**features)

    model = load_or_train_model()
    predicted_kwh = model.predict_one(features)

    return PredictOut(
        predicted_daily_kwh=float(predicted_kwh),
        scores=heuristic_scores,
        model={"type": "linear", "trained_on": model.trained_on, "rmse": model.rmse, "features": model.features},
    )
