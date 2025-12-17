## MA EV ChargeMap — EV Charging Siting Intelligence for Massachusetts

A **personal data + ML + full-stack portfolio project** that explores where new EV chargers could have the highest impact in Massachusetts cities.

- **Pilot city**: Worcester, MA
- **What you get**: interactive map + heatmap, transparent scoring model, simple ML prediction endpoint, and a clear data pipeline.

### Why this project
Siting EV chargers is a practical, high-impact problem that touches:
- **Data engineering** (ingestion + cleaning + joins + reproducible pipeline)
- **Analytics** (features, scoring, ranking, dashboards)
- **ML engineering** (train -> evaluate -> export artifact -> serve predictions)
- **Full-stack** (FastAPI APIs + Next.js UI + maps)

### Tech stack
- **Backend**: Python, FastAPI, SQLAlchemy (Postgres ready)
- **DB**: Postgres + PostGIS (via Docker)
- **Frontend**: Next.js (TypeScript), React, Tailwind CSS
- **Maps**: React Leaflet + Leaflet heatmap
- **Data/ML**: pandas, numpy, scikit-learn

### Repo layout
- `frontend/`: Next.js app (map UI)
- `backend/`: FastAPI app (APIs, scoring, ML inference)
- `data/`: ingestion + scoring scripts (raw -> processed)
- `notebooks/`: EDA + model training notebooks
- `docs/`: data sources, pipeline, scoring model, API reference

---

## Getting started (Docker)

### 1) Copy env files

```bash
cp .env.example .env
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env
```

### 2) Build and run

```bash
docker compose up --build
```

Open:
- **Frontend**: `http://localhost:3000`
- **Backend docs**: `http://localhost:8000/docs`

---

## Getting started (without Docker)

### Backend

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt

uvicorn app.main:app --reload --app-dir backend --port 8000
```

### Frontend

```bash
npm --prefix frontend install
npm --prefix frontend run dev
```

Then open `http://localhost:3000`.

---

## Data pipeline (v1)

The app can run with synthetic data, but you can also build a reproducible processed dataset:

```bash
python data/ingest_parcels.py
python data/ingest_demographics.py
python data/ingest_traffic.py
python data/build_scores.py
```

This produces:
- `data/processed/sites_worcester.json` (consumed by the backend)

Docs:
- `docs/DATA_PIPELINE.md`
- `docs/DATA_SOURCES.md`

---

## Scoring + ML

### Transparent heuristic scoring
Implemented in `backend/app/services/scoring.py`.

Docs:
- `docs/SCORING_MODEL.md`

### ML model (v1)
- A small regression model predicts daily kWh from engineered features.
- v1 is trained on synthetic / heuristic-derived labels to demonstrate the end-to-end workflow.

Where:
- Training + export notebook: `notebooks/02_model_training.ipynb`
- Runtime inference: `POST /api/predict`

---

## Tests

```bash
pip install -r backend/requirements.txt
pytest -q backend
```

---

## Notes for reviewers
- This is intentionally scoped as a **solo portfolio project**: clear structure, clean code, and transparent modeling.
- v1 uses synthetic candidate sites so the UI and API work end-to-end.
- v2 roadmap: replace synthetic layers with real GIS joins (MassGIS parcels, MAPC demographics, MassDOT traffic) and calibrate on real charger utilization data.
