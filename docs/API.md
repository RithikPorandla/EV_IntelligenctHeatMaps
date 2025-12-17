## API

The backend is a FastAPI service. Once running, interactive docs are available at `http://localhost:8000/docs`.

### `GET /api/cities`
Returns supported cities.

Example response:

```json
[
  {
    "slug": "worcester",
    "name": "Worcester, MA",
    "bbox": { "west": -71.93, "south": 42.2, "east": -71.71, "north": 42.34 }
  }
]
```

### `GET /api/sites?city={citySlug}&min_score={0..100}`
Returns candidate sites with scores.

Example:

```bash
curl "http://localhost:8000/api/sites?city=worcester&min_score=70"
```

### `GET /api/site/{id}?city={citySlug}`
Returns a detailed payload for one site.

Example:

```bash
curl "http://localhost:8000/api/site/worcester-0001?city=worcester"
```

### `POST /api/predict`
Predict daily kWh for a hypothetical location.

Example:

```bash
curl -X POST "http://localhost:8000/api/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "traffic_index": 0.8,
    "pop_density_index": 0.6,
    "renters_share": 0.5,
    "income_index": 0.4,
    "poi_index": 0.7
  }'
```

Response includes:
- `predicted_daily_kwh`: model output
- `scores`: heuristic score breakdown
- `model`: metadata about the model artifact
