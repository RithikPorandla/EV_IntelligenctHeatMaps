# Scoring (v1 heuristic)

MA EV ChargeMap starts with a transparent, replaceable heuristic scoring model. All input feature indexes are normalized to **0–1**, and output scores are scaled to **0–100**.

## Feature inputs (per candidate site)

- `traffic_index` (0–1): normalized traffic/activity near the site (MassDOT counts in future; synthetic in v1)
- `pop_density_index` (0–1): normalized population density (MAPC DataCommon / Census in future; synthetic in v1)
- `renters_share` (0–1): renter share proxying multi-unit / curbside need
- `income_index` (0–1): normalized income level (higher = higher income)
- `poi_index` (0–1): jobs/retail/schools density (OSM POIs in future; synthetic in v1)
- `parking_lot_flag` (0/1): indicates likely public parking facility (OSM/parcel in future)
- `municipal_parcel_flag` (0/1): indicates municipal ownership (parcel ownership in future)

## Component scores

### Demand potential

```text
score_demand = 100 * (0.4 * traffic_index + 0.3 * pop_density_index + 0.3 * poi_index)
```

### Equity priority

Income is inverted so **lower income increases equity priority**:

```text
score_equity = 100 * (0.5 * (1 - income_index) + 0.5 * renters_share)
```

### Traffic / activity

```text
score_traffic = 100 * traffic_index
```

### Grid / feasibility (placeholder for v1)

```text
score_grid = min(100, 50 + 25 * parking_lot_flag + 15 * municipal_parcel_flag)
```

## Overall opportunity score

```text
score_overall = 0.45 * score_demand + 0.35 * score_equity + 0.20 * score_grid
```

## Daily kWh estimate (simple, configurable constants)

```text
expected_sessions_per_day = base + alpha * traffic_index + beta * pop_density_index
daily_kwh = expected_sessions_per_day * avg_kwh_per_session
```

Default constants (see `backend/app/services/scoring.py`):

- `base = 4`
- `alpha = 8`
- `beta = 6`
- `avg_kwh_per_session = 25`

