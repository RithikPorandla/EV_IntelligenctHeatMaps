from __future__ import annotations

"""Ingest Worcester parcels (v1: sample) and generate candidate site points.

For the portfolio MVP, we treat candidate sites as point centroids.

Expected input (optional):
- data/raw/worcester_parcels_sample.csv
  Columns: parcel_id, lat, lng

If no raw file is present, this script generates a synthetic sample in that format.

Output:
- data/processed/sites_base_worcester.csv
"""

from pathlib import Path

import numpy as np
import pandas as pd

from common import RAW_DIR, PROCESSED_DIR, WORCESTER_BBOX, ensure_dirs


def _raw_path() -> Path:
    return RAW_DIR / "worcester_parcels_sample.csv"


def _generate_synthetic_parcel_centroids(n: int = 600, seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    lat = rng.uniform(WORCESTER_BBOX.south, WORCESTER_BBOX.north, size=n)
    lng = rng.uniform(WORCESTER_BBOX.west, WORCESTER_BBOX.east, size=n)

    return pd.DataFrame(
        {
            "city_slug": "worcester",
            "site_id": [f"worcester-{i:04d}" for i in range(n)],
            "parcel_id": [f"WORC-{100000 + i}" for i in range(n)],
            "lat": lat,
            "lng": lng,
        }
    )


def main() -> None:
    ensure_dirs()

    raw_path = _raw_path()
    if raw_path.exists():
        df = pd.read_csv(raw_path)
        missing = {"parcel_id", "lat", "lng"} - set(df.columns)
        if missing:
            raise ValueError(f"Missing columns in {raw_path}: {sorted(missing)}")

        df = df.copy()
        df["city_slug"] = "worcester"
        df["site_id"] = [f"worcester-{i:04d}" for i in range(len(df))]
    else:
        df = _generate_synthetic_parcel_centroids()
        df.to_csv(raw_path, index=False)

    out = PROCESSED_DIR / "sites_base_worcester.csv"
    df.to_csv(out, index=False)
    print(f"Wrote {len(df):,} candidate sites → {out}")


if __name__ == "__main__":
    main()
