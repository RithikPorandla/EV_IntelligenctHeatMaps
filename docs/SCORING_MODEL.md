# Scoring Model Documentation

This document explains the methodology for scoring EV charging site opportunities in MA EV ChargeMap.

---

## Overview

The scoring system evaluates candidate locations across **four dimensions** and combines them into an **overall opportunity score**. Additionally, a **machine learning model** predicts expected daily charging demand.

### Design Principles

1. **Transparency**: All formulas are explicit and documented
2. **Interpretability**: Clear relationship between inputs and outputs
3. **Configurability**: Weights can be adjusted for different priorities
4. **Validation**: Tested with synthetic data, ready for real data

---

## Input Features

All input features are normalized to the **0-1 range** for consistent scoring:

| Feature | Description | Range | Source |
|---------|-------------|-------|--------|
| `traffic_index` | Traffic volume near site | 0-1 | MassDOT traffic counts |
| `pop_density_index` | Population density | 0-1 | Census/MAPC data |
| `renters_share` | Fraction of renter households | 0-1 | Census ACS |
| `income_index` | Income level (0=low, 1=high) | 0-1 | Census median household income |
| `poi_index` | Points of interest density | 0-1 | OpenStreetMap |
| `parking_lot_flag` | Site has parking lot | 0 or 1 | Parcel data / OSM |
| `municipal_parcel_flag` | Municipal property | 0 or 1 | Parcel ownership |

### Normalization

Features are normalized using min-max scaling:

```
normalized = (value - min) / (max - min)
```

For spatial features (traffic, population, POI), normalization is done within the city to capture local variation.

---

## Scoring Formulas

### 1. Demand Score

**Purpose**: Estimate charging demand based on activity and traffic

**Formula**:
```
score_demand = 0.4 × traffic_index + 0.3 × pop_density_index + 0.3 × poi_index
```

**Scaled to**: 0-100

**Rationale**:
- **Traffic (40%)**: Most important indicator of vehicle presence
- **Population (30%)**: Residential charging demand
- **POI (30%)**: Commercial/activity-based demand

**Interpretation**:
- **80-100**: High-demand location (busy commercial area, major corridor)
- **60-80**: Good demand (residential area with amenities)
- **40-60**: Moderate demand
- **< 40**: Lower demand (residential-only, low traffic)

---

### 2. Equity Score

**Purpose**: Prioritize underserved communities

**Formula**:
```
score_equity = 0.5 × (1 - income_index) + 0.5 × renters_share
```

**Scaled to**: 0-100

**Rationale**:
- **Income (50%)**: Lower-income areas often lack charging access
  - **Inverted** so higher score = lower income
- **Renters (50%)**: Renters can't install home chargers
  - Higher renter share = greater public charging need

**Interpretation**:
- **80-100**: High equity priority (low-income, high renter concentration)
- **60-80**: Good equity target
- **40-60**: Mixed-income area
- **< 40**: Affluent area with home charging access

**Equity Considerations**:
- Aligns with MA environmental justice goals
- Ensures EV infrastructure reaches all communities
- Supports MOR-EV program objectives

---

### 3. Traffic Score

**Purpose**: Direct indicator of vehicle activity

**Formula**:
```
score_traffic = traffic_index × 100
```

**Scaled to**: 0-100

**Rationale**:
- Simple passthrough of traffic index
- Higher traffic = more potential charging sessions
- Useful for highway corridor sites

---

### 4. Grid Score

**Purpose**: Assess infrastructure readiness

**Formula (v1 - simplified)**:
```
base_score = 50
if parking_lot_flag: base_score += 25
if municipal_parcel_flag: base_score += 15
score_grid = min(base_score, 100)
```

**Scaled to**: 0-100

**Rationale**:
- **Baseline (50)**: Assume reasonable electrical access
- **Parking lot (+25)**: Existing infrastructure, easier permitting
- **Municipal (+15)**: Public property, aligned incentives

**Future Enhancements**:
- Proximity to electrical infrastructure (transformers, substations)
- Commercial zoning (easier permitting)
- Existing EV chargers nearby (avoid over-saturation)

---

### 5. Overall Score

**Purpose**: Balanced site opportunity metric

**Formula**:
```
score_overall = 0.45 × score_demand + 0.35 × score_equity + 0.20 × score_grid
```

**Scaled to**: 0-100

**Weight Rationale**:
- **Demand (45%)**: Primary driver of charger utilization
- **Equity (35%)**: Policy priority, social impact
- **Grid (20%)**: Infrastructure feasibility

**Interpretation**:
- **80-100**: Excellent opportunity (high-priority site)
- **60-80**: Good opportunity (recommended for consideration)
- **40-60**: Moderate opportunity
- **< 40**: Lower priority

**Weight Tuning**:

The weights can be adjusted based on stakeholder priorities:

| Scenario | Demand | Equity | Grid |
|----------|--------|--------|------|
| **Revenue-focused** | 60% | 20% | 20% |
| **Equity-focused** | 30% | 50% | 20% |
| **Balanced (current)** | 45% | 35% | 20% |

---

## Daily kWh Estimate

### Heuristic Model

**Formula**:
```
sessions_per_day = 4 + 8 × traffic_index + 6 × pop_density_index
daily_kwh_estimate = sessions_per_day × 25 kWh/session
```

**Parameters**:
- **Base sessions**: 4 (minimum daily utilization)
- **Traffic multiplier**: 8 (high traffic → more sessions)
- **Population multiplier**: 6 (dense area → more sessions)
- **kWh per session**: 25 (typical partial charge)

**Rationale**:
- Based on industry estimates of public charging patterns
- 25 kWh ≈ 80-100 miles of range (typical top-up)
- Linear model for interpretability

**Example**:
```
traffic_index = 0.7, pop_density_index = 0.6

sessions = 4 + 8(0.7) + 6(0.6) = 4 + 5.6 + 3.6 = 13.2
daily_kwh = 13.2 × 25 = 330 kWh/day
```

---

## Machine Learning Model

### Purpose

The ML model provides a data-driven prediction of daily kWh demand, learning patterns from site features.

### Model Type

**Random Forest Regressor** (or Gradient Boosting)

**Why?**
- Handles non-linear relationships
- Captures feature interactions
- Provides feature importance rankings
- Robust to outliers

### Training Data

**Features** (7):
- `traffic_index`
- `pop_density_index`
- `renters_share`
- `income_index`
- `poi_index`
- `parking_lot_flag`
- `municipal_parcel_flag`

**Target**:
- `daily_kwh_estimate` (computed from heuristic initially)

**Training Process** (see `notebooks/02_model_training.ipynb`):
1. Load site data from database
2. Prepare feature matrix X and target vector y
3. Split into train (80%) and test (20%)
4. Train multiple models (Linear, Random Forest, Gradient Boosting)
5. Evaluate with R², RMSE, MAE
6. Select best model based on test performance
7. Retrain on full dataset
8. Export model as `.pkl` file

### Model Performance

**Expected Metrics** (on synthetic data):
- **R² Score**: ~0.85-0.95 (strong predictive power)
- **RMSE**: ~15-25 kWh/day
- **MAE**: ~10-20 kWh/day

### Feature Importance

Typical importance ranking (from Random Forest):
1. **traffic_index** (~30-40%): Most predictive feature
2. **pop_density_index** (~25-30%): Strong secondary predictor
3. **poi_index** (~15-20%): Activity indicator
4. **income_index** (~5-10%): Indirect demand signal
5. Other features (~5-10% combined)

### Deployment

The trained model is:
1. Saved to `models/site_score_model.pkl`
2. Loaded by backend on startup
3. Used in `/api/predict` endpoint
4. Falls back to heuristic if model unavailable

---

## Validation & Testing

### Unit Tests

Tests in `backend/tests/test_scoring.py`:
- Formula correctness
- Edge cases (0, 1, boundary values)
- Equity score inversion (low income = high score)
- Score ranges (0-100)

### Integration Tests

API tests in `backend/tests/test_api.py`:
- `/api/predict` endpoint validation
- Input range checking
- Output format verification

### Sensitivity Analysis

**Demand Score Sensitivity**:
- Varying traffic ±0.1 → score change ±4.0
- Relatively stable to small feature changes

**Equity Score Sensitivity**:
- Income -0.2 → equity +10.0 (significant)
- Design intentionally sensitive to equity factors

---

## Limitations & Future Work

### Current Limitations

1. **Synthetic Training Data**: ML model trained on simulated data
   - In production, train on real charger usage data
   
2. **Static Model**: No temporal features
   - Future: time-of-day, day-of-week, seasonal patterns
   
3. **Simplified Grid Score**: Placeholder logic
   - Future: integrate utility infrastructure GIS data
   
4. **Linear Demand Model**: Basic heuristic
   - Real data would reveal more complex patterns

### Future Enhancements

1. **Real Utilization Data**
   - Partner with ChargePoint, EVgo, etc. for actual usage data
   - Retrain model on real kWh dispensed
   
2. **Temporal Modeling**
   - Predict by hour, day, season
   - Account for commute patterns, weekend vs. weekday
   
3. **Network Effects**
   - Consider existing charger density
   - Optimize for network coverage, not just individual sites
   
4. **Cost-Benefit Analysis**
   - Installation costs by site type
   - Revenue projections
   - Payback period calculations
   
5. **Live Model Updates**
   - Retrain periodically as new data arrives
   - A/B test scoring formula variations

---

## References

### Methodology Influences
- DOE Alternative Fuel Corridor guidance
- NREL EVI-Pro model (EV infrastructure planning)
- California Energy Commission DCFC planning methodology
- Academic papers on EV adoption and charging behavior

### MA Policy Context
- MA 2050 Decarbonization Roadmap
- EV incentive programs (MOR-EV, MassEVIP)
- Environmental justice designations

---

## Code Reference

**Heuristic Scoring**:
- `backend/app/services/scoring.py`

**ML Model**:
- Training: `notebooks/02_model_training.ipynb`
- Deployment: `backend/app/services/ml_predictor.py`

**Tests**:
- `backend/tests/test_scoring.py`

---

**Summary**: The MA EV ChargeMap scoring model combines transparent heuristics with machine learning to identify high-opportunity EV charging sites, balancing demand, equity, and infrastructure considerations.
