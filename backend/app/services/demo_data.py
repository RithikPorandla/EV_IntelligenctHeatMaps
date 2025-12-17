"""
Demo data seeding for the prototype.

Goal: make `docker-compose up` feel "end-to-end" by ensuring Worcester has
some candidate sites + scores the first time the app starts.

This is intentionally simple and deterministic-ish, and should be replaced by
the real `/data/*` pipeline + PostGIS workflows as the project evolves.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Tuple

import numpy as np
from sqlalchemy.orm import Session

from app.models.site import Site
from app.services.scoring import ScoringService


@dataclass(frozen=True)
class BBox:
    west: float
    south: float
    east: float
    north: float


WORCESTER_BBOX = BBox(
    west=-71.8744,
    south=42.2084,
    east=-71.7277,
    north=42.3126,
)

WORCESTER_CENTER: Tuple[float, float] = (42.2626, -71.8023)  # (lat, lng)


def _distance_to_center(lat: float, lng: float) -> float:
    dlat = lat - WORCESTER_CENTER[0]
    dlng = lng - WORCESTER_CENTER[1]
    return float(np.sqrt(dlat * dlat + dlng * dlng))


def _label(lat: float, lng: float) -> str:
    ns = "North" if lat > WORCESTER_CENTER[0] else "South"
    ew = "East" if lng > WORCESTER_CENTER[1] else "West"
    return f"Worcester {ns}-{ew} (Seeded)"


def _generate_points(n: int, rng: np.random.Generator) -> List[Tuple[float, float]]:
    lats = rng.uniform(WORCESTER_BBOX.south, WORCESTER_BBOX.north, size=n)
    lngs = rng.uniform(WORCESTER_BBOX.west, WORCESTER_BBOX.east, size=n)
    return list(zip(lats.tolist(), lngs.tolist()))


def seed_worcester_if_empty(db: Session, n_sites: int = 600) -> int:
    """
    Seed Worcester demo sites only if none exist.

    Returns number of inserted sites (0 if already present).
    """
    existing = db.query(Site).filter(Site.city == "worcester").count()
    if existing > 0:
        return 0

    rng = np.random.default_rng(42)
    points = _generate_points(n_sites, rng)

    sites: List[Site] = []
    for i, (lat, lng) in enumerate(points, start=1):
        dist = _distance_to_center(lat, lng)

        # Simple, locally-correlated synthetic feature indexes
        traffic_index = float(np.clip(1.0 - dist * 8.0 + rng.normal(0, 0.08), 0, 1))
        pop_density_index = float(np.clip(1.0 - dist * 10.0 + rng.normal(0, 0.10), 0, 1))
        poi_index = float(np.clip(0.6 * traffic_index + 0.4 * pop_density_index + rng.normal(0, 0.08), 0, 1))

        # Equity features: west/east income gradient + renters correlated to density
        west_bias = (lng - WORCESTER_CENTER[1]) * 5.0
        income_index = float(np.clip(0.5 + west_bias + rng.normal(0, 0.18), 0, 1))
        renters_share = float(np.clip(0.3 + 0.4 * pop_density_index + 0.2 * (1 - income_index) + rng.normal(0, 0.10), 0, 1))

        # Feasibility flags
        parking_lot_flag = int(rng.random() < (0.25 + 0.35 * poi_index))
        municipal_parcel_flag = int(rng.random() < 0.10)

        scores = ScoringService.compute_all_scores(
            {
                "traffic_index": traffic_index,
                "pop_density_index": pop_density_index,
                "renters_share": renters_share,
                "income_index": income_index,
                "poi_index": poi_index,
                "parking_lot_flag": parking_lot_flag,
                "municipal_parcel_flag": municipal_parcel_flag,
            }
        )

        sites.append(
            Site(
                city="worcester",
                lat=float(lat),
                lng=float(lng),
                location_label=_label(lat, lng),
                parcel_id=f"WORC-SEED-{i:04d}",
                traffic_index=round(traffic_index, 3),
                pop_density_index=round(pop_density_index, 3),
                renters_share=round(renters_share, 3),
                income_index=round(income_index, 3),
                poi_index=round(poi_index, 3),
                parking_lot_flag=parking_lot_flag,
                municipal_parcel_flag=municipal_parcel_flag,
                score_demand=round(scores["score_demand"], 1),
                score_equity=round(scores["score_equity"], 1),
                score_traffic=round(scores["score_traffic"], 1),
                score_grid=round(scores["score_grid"], 1),
                score_overall=round(scores["score_overall"], 1),
                daily_kwh_estimate=round(scores["daily_kwh_estimate"], 1),
            )
        )

    db.bulk_save_objects(sites)
    db.commit()
    return len(sites)

