from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path

import numpy as np

from app.services.cities import City
from app.services.scoring import compute_all_scores


@dataclass(frozen=True)
class SiteRecord:
    id: str
    city_slug: str
    lat: float
    lng: float
    location_label: str | None
    parcel_id: str | None

    traffic_index: float
    pop_density_index: float
    renters_share: float
    income_index: float
    poi_index: float

    score_overall: float
    score_demand: float
    score_equity: float
    score_traffic: float
    score_grid: float
    daily_kwh_estimate: float


def _processed_sites_path(city_slug: str) -> Path:
    # Prefer explicit configuration; otherwise auto-detect.
    env_dir = os.getenv("PROCESSED_DATA_DIR")
    candidates: list[Path] = []
    if env_dir:
        candidates.append(Path(env_dir))

    # docker-compose mounts processed data here by default
    candidates.append(Path("/data/processed"))

    # local dev: repo_root/data/processed
    # file: backend/app/services/site_repository.py -> repo_root is 4 parents up
    try:
        repo_root = Path(__file__).resolve().parents[4]
        candidates.append(repo_root / "data" / "processed")
    except IndexError:
        pass

    processed_dir = next((p for p in candidates if p.exists()), candidates[-1])
    return processed_dir / f"sites_{city_slug}.json"


def _load_processed_sites(city_slug: str) -> list[SiteRecord] | None:
    path = _processed_sites_path(city_slug)
    if not path.exists():
        return None

    with path.open("r", encoding="utf-8") as f:
        raw = json.load(f)

    sites: list[SiteRecord] = []
    for row in raw:
        sites.append(
            SiteRecord(
                id=str(row["id"]),
                city_slug=str(row["city_slug"]),
                lat=float(row["lat"]),
                lng=float(row["lng"]),
                location_label=row.get("location_label"),
                parcel_id=row.get("parcel_id"),
                traffic_index=float(row["traffic_index"]),
                pop_density_index=float(row["pop_density_index"]),
                renters_share=float(row["renters_share"]),
                income_index=float(row["income_index"]),
                poi_index=float(row["poi_index"]),
                score_overall=float(row["score_overall"]),
                score_demand=float(row["score_demand"]),
                score_equity=float(row["score_equity"]),
                score_traffic=float(row["score_traffic"]),
                score_grid=float(row["score_grid"]),
                daily_kwh_estimate=float(row["daily_kwh_estimate"]),
            )
        )
    return sites


def generate_synthetic_sites(city: City, *, n: int = 600, seed: int = 42) -> list[SiteRecord]:
    """Generate a synthetic candidate-site layer for prototyping.

    This lets the full-stack app work end-to-end before real GIS ingestion is done.
    """

    rng = np.random.default_rng(seed)

    lats = rng.uniform(city.south, city.north, size=n)
    lngs = rng.uniform(city.west, city.east, size=n)

    # Create spatial-ish gradients to make the heatmap visually meaningful
    # (higher traffic near a synthetic "downtown" point)
    downtown_lat = (city.south + city.north) / 2.0
    downtown_lng = (city.west + city.east) / 2.0

    dist = np.sqrt((lats - downtown_lat) ** 2 + (lngs - downtown_lng) ** 2)
    dist_norm = (dist - dist.min()) / (dist.max() - dist.min() + 1e-9)

    traffic_index = np.clip(1.0 - dist_norm + rng.normal(0, 0.08, size=n), 0, 1)
    pop_density_index = np.clip(1.0 - 0.8 * dist_norm + rng.normal(0, 0.10, size=n), 0, 1)
    poi_index = np.clip(1.0 - 0.9 * dist_norm + rng.normal(0, 0.10, size=n), 0, 1)

    renters_share = np.clip(0.35 + 0.35 * (1.0 - dist_norm) + rng.normal(0, 0.08, size=n), 0, 1)
    income_index = np.clip(0.60 + 0.20 * dist_norm + rng.normal(0, 0.07, size=n), 0, 1)

    sites: list[SiteRecord] = []
    for i in range(n):
        features = {
            "traffic_index": float(traffic_index[i]),
            "pop_density_index": float(pop_density_index[i]),
            "renters_share": float(renters_share[i]),
            "income_index": float(income_index[i]),
            "poi_index": float(poi_index[i]),
        }
        scores = compute_all_scores(**features)
        sites.append(
            SiteRecord(
                id=f"{city.slug}-{i:04d}",
                city_slug=city.slug,
                lat=float(lats[i]),
                lng=float(lngs[i]),
                location_label=None,
                parcel_id=None,
                **features,
                **scores,
            )
        )

    return sites


def get_sites_for_city(city: City) -> list[SiteRecord]:
    processed = _load_processed_sites(city.slug)
    if processed is not None:
        return processed
    return generate_synthetic_sites(city)


def get_site_by_id(city: City, site_id: str) -> SiteRecord | None:
    for s in get_sites_for_city(city):
        if s.id == site_id:
            return s
    return None
