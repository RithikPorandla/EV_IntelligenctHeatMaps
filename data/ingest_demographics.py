from __future__ import annotations

"""Ingest demographics / equity features (v1: synthetic).

In v2, this script should join MAPC DataCommon attributes (tract/block group)
onto candidate sites. For the MVP we generate plausible values, but keep the
schema and data engineering steps realistic.

Input:
- data/processed/sites_base_worcester.csv

Output:
- data/processed/demographics_worcester.csv
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

    # Make a gentle spatial gradient: closer to synthetic downtown has higher renter share
    lat_mid = (WORCESTER_BBOX.south + WORCESTER_BBOX.north) / 2
    lng_mid = (WORCESTER_BBOX.west + WORCESTER_BBOX.east) / 2
    dist = np.sqrt((sites["lat"] - lat_mid) ** 2 + (sites["lng"] - lng_mid) ** 2)
    dist_norm = (dist - dist.min()) / (dist.max() - dist.min() + 1e-9)

    rng = np.random.default_rng(13)

    renters_share = np.clip(0.35 + 0.35 * (1.0 - dist_norm) + rng.normal(0, 0.08, size=len(sites)), 0, 1)
    income_index = np.clip(0.60 + 0.20 * dist_norm + rng.normal(0, 0.07, size=len(sites)), 0, 1)
    pop_density_index = np.clip(1.0 - 0.8 * dist_norm + rng.normal(0, 0.10, size=len(sites)), 0, 1)

    out = pd.DataFrame(
        {
            "site_id": sites["site_id"],
            "renters_share": renters_share,
            "income_index": income_index,
            "pop_density_index": pop_density_index,
        }
    )

    out_path = PROCESSED_DIR / "demographics_worcester.csv"
    out.to_csv(out_path, index=False)
    print(f"Wrote demographics → {out_path}")


if __name__ == "__main__":
    main()
