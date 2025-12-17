# API Reference

The backend is built with FastAPI. Interactive docs are available at `/docs` when running locally.

## Endpoints

### `GET /api/cities`
Returns a list of supported cities.
- **Response**: `[{"slug": "worcester", "name": "Worcester, MA", "bbox": [...]}]`

### `GET /api/sites?city=worcester`
Returns all candidate sites for a city with their pre-calculated scores.
- **Query Param**: `city` (string)
- **Response**: Array of site objects.
  ```json
  [
    {
      "id": "site-0",
      "lat": 42.26,
      "lng": -71.80,
      "score_overall": 75.5,
      ...
    }
  ]
  ```

### `GET /api/site/{id}`
Returns detailed information for a specific site.
- **Response**: Site object with `features` dictionary and `notes`.

### `POST /api/predict`
Predicts scores and demand for a hypothetical location.
- **Body**:
  ```json
  {
    "traffic_index": 0.8,
    "pop_density_index": 0.6,
    "renters_share": 0.5,
    "income_index": 0.4,
    "poi_index": 0.7
  }
  ```
- **Response**:
  ```json
  {
    "score_overall": 82.0,
    "daily_kwh_estimate": 350.5,
    "component_scores": { ... }
  }
  ```
