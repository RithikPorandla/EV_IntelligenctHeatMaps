from __future__ import annotations

"""Build final site scores used by the API.

This joins:
- sites_base (candidate points)
- demographics (equity + density features)
- traffic (traffic + POI features)

Then computes the transparent heuristic scores described in docs/SCORING_MODEL.md.

Outputs:
- data/processed/sites_worcester.json

Note: This output is deliberately JSON (not pickle/binary) so it's easy to review.
"""

import json
from pathlib import Path

import numpy as np
import pandas as pd

from common import PROCESSED_DIR, ensure_dirs


def clamp01(x: float) -> float:
    return float(max(0.0, min(1.0, float(x))))


def compute_scores(*, traffic_index: float, pop_density_index: float, renters_share: float, income_index: float, poi_index: float) -> dict[str, float]:
    traffic_index = clamp01(traffic_index)
    pop_density_index = clamp01(pop_density_index)
    renters_share = clamp01(renters_share)
    income_index = clamp01(income_index)
    poi_index = clamp01(poi_index)

    score_demand = 100.0 * clamp01(0.4 * traffic_index + 0.3 * pop_density_index + 0.3 * poi_index)
    score_equity = 100.0 * clamp01(0.5 * (1.0 - income_index) + 0.5 * renters_share)
    score_traffic = 100.0 * clamp01(traffic_index)
    score_grid = 100.0 * clamp01(traffic_index)  # placeholder

    score_overall = 100.0 * clamp01(0.45 * (score_demand / 100.0) + 0.35 * (score_equity / 100.0) + 0.20 * (score_grid / 100.0))

    expected_sessions = 4.0 + 8.0 * traffic_index + 6.0 * pop_density_index
    daily_kwh_estimate = float(expected_sessions * 25.0)

    return {
        "score_overall": float(score_overall),
        "score_demand": float(score_demand),
        "score_equity": float(score_equity),
        "score_traffic": float(score_traffic),
        "score_grid": float(score_grid),
        "daily_kwh_estimate": float(daily_kwh_estimate),
    }


def main() -> None:
    ensure_dirs()

    base_path = PROCESSED_DIR / "sites_base_worcester.csv"
    demo_path = PROCESSED_DIR / "demographics_worcester.csv"
    traffic_path = PROCESSED_DIR / "traffic_worcester.csv"

    missing = [p for p in [base_path, demo_path, traffic_path] if not p.exists()]
    if missing:
        raise FileNotFoundError(
            "Missing processed inputs. Run:\n"
            "  python data/ingest_parcels.py\n"
            "  python data/ingest_demographics.py\n"
            "  python data/ingest_traffic.py\n"
            f"Missing: {', '.join(str(p) for p in missing)}"
        )

    base = pd.read_csv(base_path)
    demo = pd.read_csv(demo_path)
    traffic = pd.read_csv(traffic_path)

    df = base.merge(demo, on="site_id", how="left").merge(traffic, on="site_id", how="left")

    for col in ["traffic_index", "pop_density_index", "renters_share", "income_index", "poi_index"]:
        df[col] = df[col].fillna(df[col].median())
        df[col] = df[col].clip(lower=0.0, upper=1.0)

    scores = df.apply(
        lambda r: compute_scores(
            traffic_index=float(r["traffic_index"]),
            pop_density_index=float(r["pop_density_index"]),
            renters_share=float(r["renters_share"]),
            income_index=float(r["income_index"]),
            poi_index=float(r["poi_index"]),
        ),
        axis=1,
        result_type="expand",
    )

    df = pd.concat([df, scores], axis=1)

    # Sort for stable output (useful for diffs)
    df = df.sort_values("site_id").reset_index(drop=True)

    out_rows = []
    for _, r in df.iterrows():
        out_rows.append(
            {
                "id": str(r["site_id"]),
                "city_slug": str(r["city_slug"]),
                "lat": float(r["lat"]),
                "lng": float(r["lng"]),
                "location_label": None,
                "parcel_id": str(r["parcel_id"]) if not pd.isna(r["parcel_id"]) else None,
                "traffic_index": float(r["traffic_index"]),
                "pop_density_index": float(r["pop_density_index"]),
                "renters_share": float(r["renters_share"]),
                "income_index": float(r["income_index"]),
                "poi_index": float(r["poi_index"]),
                "score_overall": float(r["score_overall"]),
                "score_demand": float(r["score_demand"]),
                "score_equity": float(r["score_equity"]),
                "score_traffic": float(r["score_traffic"]),
                "score_grid": float(r["score_grid"]),
                "daily_kwh_estimate": float(r["daily_kwh_estimate"]),
            }
        )

    out_path = PROCESSED_DIR / "sites_worcester.json"
    with Path(out_path).open("w", encoding="utf-8") as f:
        json.dump(out_rows, f, indent=2)

    print(f"Wrote scored sites → {out_path} ({len(out_rows):,} rows)")


if __name__ == "__main__":
    main()
