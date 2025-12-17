# Scoring Model & Machine Learning

The "EV Charging Opportunity Score" is a composite metric designed to highlight the best locations for new infrastructure.

## Heuristic Scoring

We define three sub-scores, each normalized from 0 to 100:

1. **Demand Score**:
   - Formula: `0.4 * Traffic_Index + 0.3 * Pop_Density + 0.3 * POI_Index`
   - Goal: Target areas with high utilization potential.

2. **Equity Score**:
   - Formula: `0.5 * (1 - Income_Index) + 0.5 * Renter_Share`
   - Goal: Prioritize areas with lower private charging access (renters) and underserved communities.

3. **Traffic Score**:
   - Formula: `Traffic_Index` (Raw normalized AADT)
   - Goal: Visibility and pass-by traffic.

**Overall Score**:
- `0.45 * Demand + 0.35 * Equity + 0.20 * Grid/Traffic`

## Machine Learning Model

To estimate **Daily kWh Demand** (a regression task), we use a **RandomForestRegressor**.

### Features
- `traffic_index` (0-1)
- `pop_density_index` (0-1)
- `renters_share` (0-1)
- `income_index` (0-1)
- `poi_index` (0-1)

### Training
- **Data**: Currently trained on a synthetic dataset (`notebooks/train_model.py`) that simulates the relationships found in real-world utilization studies (e.g., higher traffic -> higher usage).
- **Target**: `daily_kwh` (simulated based on weighted features + noise).
- **Performance**: The model achieves an R² of ~0.70 on the synthetic holdout set.

### Usage
The model is serialized via `joblib` to `models/site_score_model.pkl` and loaded by the FastAPI backend to provide real-time estimates for custom site inputs (`POST /api/predict`).
