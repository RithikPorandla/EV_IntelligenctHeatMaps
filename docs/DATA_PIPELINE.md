# Data Pipeline

The data pipeline consists of standalone Python scripts located in `/data`.

## Scripts

1. **`ingest_parcels.py`**
   - **Input**: `data/raw/worcester_parcels_sample.csv` (Mock CSV/WKT data).
   - **Process**: Parses geometry (WKT) to calculate centroids for site candidates.
   - **Output**: `data/processed/sites.csv`.

2. **`ingest_demographics.py`** (Planned)
   - Loads MAPC CSVs and normalizes census tract data.

3. **`ingest_traffic.py`** (Planned)
   - Spatial join of sites to nearest MassDOT traffic count stations.

4. **`build_scores.py`** (Planned)
   - Merges processed datasets and computes heuristic scores before saving to the database/API source.

## Usage

To run the parcel ingestion:
```bash
python data/ingest_parcels.py
```
