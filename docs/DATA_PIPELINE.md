## Data pipeline (v1)

The pipeline is intentionally simple and transparent.

### Folder conventions
- `data/raw/`: manually downloaded CSV/GeoJSON from public portals (or small samples)
- `data/processed/`: cleaned/engineered outputs consumed by the backend API

### Scripts
Run these from the repo root.

1) **Candidate sites**

```bash
python data/ingest_parcels.py
```

- Reads `data/raw/worcester_parcels_sample.csv` if present.
- Otherwise generates a sample file with `parcel_id, lat, lng`.
- Writes `data/processed/sites_base_worcester.csv`.

2) **Demographics (equity + density)**

```bash
python data/ingest_demographics.py
```

- v1: generates plausible values.
- v2: join MAPC DataCommon attributes by tract/block group.
- Writes `data/processed/demographics_worcester.csv`.

3) **Traffic + activity**

```bash
python data/ingest_traffic.py
```

- v1: generates plausible values.
- v2: nearest-neighbor join from MassDOT traffic inventory (AADT).
- Writes `data/processed/traffic_worcester.csv`.

4) **Score building**

```bash
python data/build_scores.py
```

- Joins base + demographics + traffic.
- Computes indices and heuristic scores.
- Writes `data/processed/sites_worcester.json`.

### How the app uses processed data
- The FastAPI backend loads `data/processed/sites_{city}.json` if present.
- If missing, it falls back to a synthetic generator so the UI works end-to-end.
