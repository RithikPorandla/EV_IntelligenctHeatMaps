## Scoring model (transparent heuristics + small ML component)

This project uses two modeling layers:

- **Heuristic scores**: fully transparent, designed to be readable and editable.
- **ML predictor (v1)**: a small regression model that predicts daily kWh from engineered features.

> Portfolio note: v1 is trained on **synthetic / heuristic-derived labels**. The goal is to demonstrate end-to-end ML engineering (training -> evaluation -> export -> API inference), not claim real-world accuracy.

### Features per site
All features are normalized to **[0, 1]**.

- `traffic_index`
- `pop_density_index`
- `renters_share`
- `income_index` (1 = highest income)
- `poi_index`

### Heuristic scores
All scores are **[0, 100]**.

#### Demand
\[
\text{score\_demand} = 100 \cdot (0.4\,t + 0.3\,p + 0.3\,poi)
\]

#### Equity
\[
\text{score\_equity} = 100 \cdot (0.5\,(1 - income) + 0.5\,renters)
\]

#### Traffic
\[
\text{score\_traffic} = 100 \cdot t
\]

#### Grid (placeholder)
In v1, `score_grid` is a placeholder tied to `traffic_index`. In v2 it should incorporate zoning, parking, public land, and constraint layers.

#### Overall
\[
\text{score\_overall} = 100 \cdot (0.45\,demand + 0.35\,equity + 0.20\,grid)
\]

### Daily kWh estimate (heuristic)
We estimate sessions/day and multiply by an average kWh per session.

- `base = 4`
- `alpha = 8`
- `beta = 6`
- `avg_kWh_per_session = 25`

\[
\text{sessions/day} = base + \alpha\,t + \beta\,p
\]
\[
\text{daily\_kwh\_estimate} = \text{sessions/day} \cdot 25
\]

### ML model (v1)
- **Type**: linear regression (Ridge)
- **Target**: daily kWh (heuristic label + noise)
- **Export**: JSON artifact (`backend/models/site_demand_model.json`) containing weights and intercept

Where to look:
- Training plumbing (backend): `backend/app/services/ml_model.py`
- Notebook: `notebooks/02_model_training.ipynb`
- API endpoint: `POST /api/predict`

### Limitations (intentional for v1)
- No real utilization labels yet (kWh dispensed / sessions per charger)
- Candidate sites are points (no parcel polygons / zoning constraints)
- No spatial joins (tract/block group, road proximity) yet

### Next improvements (v2)
- Replace synthetic features with real joins (MAPC, MassDOT, MassGIS)
- Use PostGIS + spatial indexing
- Calibrate model on real charger utilization (if accessible)
- Add constraint layers (parking, zoning, existing charger coverage)
