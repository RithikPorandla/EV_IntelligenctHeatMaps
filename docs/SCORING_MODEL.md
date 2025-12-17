# Scoring Model (v1 Heuristic)

The site suitability score is a composite of three main factors: **Demand**, **Equity**, and **Grid/Feasibility**.

All inputs are normalized to a 0–1 scale.

## Formulas

### 1. Demand Score (40-50% weight)
Represents the potential utilization of the charger.

```python
score_demand = 0.4 * traffic_index + 0.3 * pop_density_index + 0.3 * poi_index
```
- `traffic_index`: Normalized nearby traffic volume.
- `pop_density_index`: Normalized residential density.
- `poi_index`: Density of jobs, retail, and amenities.

### 2. Equity Score (30-40% weight)
Prioritizes underserved communities.

```python
score_equity = 0.5 * (1 - income_index) + 0.5 * renters_share
```
- `income_index`: Normalized Median Household Income (inverted so lower income = higher score).
- `renters_share`: Percentage of housing units that are renter-occupied (proxy for lack of home charging).

### 3. Traffic / Grid Score (20% weight)
(Currently simplified)

```python
score_grid = 0.5 * traffic_index + 0.5 * grid_proximity_proxy
```

### Overall Score
```python
score_overall = 0.45 * score_demand + 0.35 * score_equity + 0.20 * score_grid
```

## Load Estimation
We estimate daily energy delivery (kWh) using a simple linear model:

```python
daily_kWh = (Base + 8 * traffic_index + 6 * pop_density_index) * 25 kWh/session
```
