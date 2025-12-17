# API Documentation

Base URL: `http://localhost:8000/api`

## Endpoints

### `GET /cities`
Returns list of supported cities and their metadata (center, zoom).

**Response:**
```json
[
  {
    "slug": "worcester",
    "name": "Worcester, MA",
    "center": [42.2626, -71.8023],
    "zoom": 13
  }
]
```

### `GET /sites`
Returns candidate sites for a city.

**Query Params:**
- `city`: (string) e.g., "worcester"

**Response:**
```json
[
  {
    "id": 1,
    "city_slug": "worcester",
    "lat": 42.26,
    "lng": -71.80,
    "score_overall": 85.5,
    "score_demand": 80.0,
    ...
  }
]
```

### `GET /site/{id}`
Returns detailed information for a specific site.

### `POST /predict`
Calculates scores for a new location based on provided features.

**Body:**
```json
{
  "traffic_index": 0.8,
  "pop_density_index": 0.5,
  "renters_share": 0.6,
  "income_index": 0.4,
  "poi_index": 0.7
}
```
