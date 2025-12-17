from __future__ import annotations

"""Ingest traffic data (v1: synthetic).

In v2, download MassDOT traffic inventory (AADT points/segments) and compute a
nearest-neighbor join to candidate sites.

Input:
- data/processed/sites_base_worcester.csv

Output:
- data/processed/traffic_worcester.csv
"""

import numpy as np
import pandas as pd

from common import PROCESSED_DIR, WORCESTER_BBOX, ensure_dirs


def main() -> None:
    ensure_dirs()

    base_path = PROCESSED_DIR / "sites_base_worcester.csv"
    if not base_path.exists():
        raise FileNotFoundError(
            f"Missing {base_path}. Run: python data/ingest_parcels.py"
        )

    sites = pd.read_csv(base_path)

    lat_mid = (WORCESTER_BBOX.south + WORCESTER_BBOX.north) / 2
    lng_mid = (WORCESTER_BBOX.west + WORCESTER_BBOX.east) / 2
    dist = np.sqrt((sites["lat"] - lat_mid) ** 2 + (sites["lng"] - lng_mid) ** 2)
    dist_norm = (dist - dist.min()) / (dist.max() - dist.min() + 1e-9)

    rng = np.random.default_rng(9)

    traffic_index = np.clip(1.0 - dist_norm + rng.normal(0, 0.08, size=len(sites)), 0, 1)
    poi_index = np.clip(1.0 - 0.9 * dist_norm + rng.normal(0, 0.10, size=len(sites)), 0, 1)

    out = pd.DataFrame(
        {
            "site_id": sites["site_id"],
            "traffic_index": traffic_index,
            "poi_index": poi_index,
        }
    )

    out_path = PROCESSED_DIR / "traffic_worcester.csv"
    out.to_csv(out_path, index=False)
    print(f"Wrote traffic → {out_path}")


if __name__ == "__main__":
    main()
